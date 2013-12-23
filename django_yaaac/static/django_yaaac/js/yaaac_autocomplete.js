var yaaac_set_label = function() {
    /* Display the unicode() value of the instance and hide the autocomplete input. */
    var $id_input = $(this);
    if ($id_input.val() !== "") {
        $.get($id_input.attr("search_url"), {search_fields: $id_input.attr("search_fields"), pk: $id_input.val()},
              function(data){
                var $search_input = $id_input.next();
                var $lookup_elem = $search_input.next();
                var $value_container = $search_input.siblings(".yaaac_value_container");
                var $value_elem = $value_container.find(".yaaac_value");
                var $value_elem_with_link = $value_elem.find("a");
                if ($value_elem_with_link.length !== 0) {
                    $value_elem_with_link.attr("href", data.url);
                    $value_elem = $value_elem_with_link;
                }
                $value_elem.html(data.value);

                $search_input.hide();
                $lookup_elem.hide();
                $value_container.show();
        });
    }
};


var yaaac_clear_value = function() {
    /* Clear the FK field and switch to autocomplete search mode. */
    $(this).parents(".yaaac_container").find(".yaaac_pk").val("").change();
    $(this).parent().hide();
    $(this).parents(".yaaac_container").find(".yaaac_search_input").val("").show();
    $(this).parents(".yaaac_container").find(".yaaac_lookup").show();
};


var yaaac_set_autocomplete = function() {
    /* Add autocomplete if not already.
     * Attached to 'focus' event to handle inlines not present when page is loaded.
     * */
    if ($(this).autocomplete()) {
        return;
    }
    var $id_input = $(this).prev();
    var dj_opts = $.parseJSON($id_input.attr("search_opts"));
    var options = {
        minChars: dj_opts.min_chars,
        maxHeight: dj_opts.max_height,
        width: dj_opts.width,
        serviceUrl: $id_input.attr("search_url"),
        onSelect: function(suggestion) {
            $id_input.val(suggestion.data).change();
        },
        params: {
            search_fields: $id_input.attr("search_fields")
        }
    };
    $input = $(this).autocomplete(options);
    $input.autocomplete().enable();
};


var id_to_windowname = function(text) {
/* Inspired from django/contrib/admin/static/admin/js/admin/RelatedObjectsLookup.js */
    text = text.replace(/\./g, '__dot__');
    text = text.replace(/\-/g, '__dash__');
    return text;
};


var windowname_to_id = function(text) {
/* Inspired from django/contrib/admin/static/admin/js/admin/RelatedObjectsLookup.js */
    text = text.replace(/__dot__/g, '.');
    text = text.replace(/__dash__/g, '-');
    return text;
};

var yaaac_open_lookup = function() {
/* Inspired from django/contrib/admin/static/admin/js/admin/RelatedObjectsLookup.js */
    var name = $(this).attr("id").replace(/^lookup_/, '');
    name = id_to_windowname(name);
    var href = $(this).attr("href");
    // FIXME : django >= 1.6 use _popup.
    if (href.search(/\?/) >= 0) {
        href += '&' + POPUP_VAR + '=1';
    } else {
        href += '?' + POPUP_VAR + '=1';
    }
    var win = window.open(href, name, 'height=500,width=800,resizable=yes,scrollbars=yes');
    win.focus();
    return false;
};

var dismissRelatedLookupPopup = function(win, chosenId) {
/* Inspired from django/contrib/admin/static/admin/js/admin/RelatedObjectsLookup.js */
    var name = windowname_to_id(win.name);
    var $elem = $("#" + name);
    // TODO: test vManyToManyRawIdAdminField switch.
    if ($elem.hasClass('vManyToManyRawIdAdminField') && $elem.val()) {
        $elem.val($elem.val() + ',' + chosenId);
    } else {
        $elem.val(chosenId).change();
    }
    win.close();
};


$(document).ready(function() {
    $("body").on("change", ".yaaac_pk", yaaac_set_label);
    $("body").on("click", ".yaaac_clear_value", yaaac_clear_value);
    $("body").on("click", ".yaaac_lookup", yaaac_open_lookup);
    $("body").on("focus", ".yaaac_search_input", yaaac_set_autocomplete);
});
