var yaaac_set_label = function() {
    /* Display the unicode() value of the instance and hide the autocomplete input. */
    var $id_input = $(this);
    if ($id_input.val() !== "") {
        $.get($id_input.attr("search_url"), {value_attr: $id_input.attr("value_attr"), pk: $id_input.val()},
              function(data){
                var search_input = $id_input.next();
                var value_container = search_input.next();
                var value_elem = value_container.find(".yaaac_value");
                value_elem.html(data.value);

                search_input.hide();
                value_container.show();
        });
    }
};


var yaaac_clear_value = function() {
    /* Clear the FK field and switch to autocomplete search mode. */
    $(this).parents(".yaaac_container").find(".yaaac_pk").val("");
    $(this).parent().hide();
    $(this).parents(".yaaac_container").find(".yaaac_search_input").val("").show();
};


$(document).ready(function() {
    $(".yaaac_pk").on("change", yaaac_set_label);
    $(".yaaac_clear_value").on("click", yaaac_clear_value);

    $(".yaaac_search_input").each(function() {
        // $id_input is the input.yaaac_pk elem.
        $id_input = $(this).prev();
        var options = {
            serviceUrl: $id_input.attr("search_url"),
            onSelect: function(suggestion) {
                $id_input.val(suggestion.data).change();
            },
            params: {
                value_attr: $id_input.attr("value_attr")
            }
        };
        $input = $(this).autocomplete(options);
    });
});
