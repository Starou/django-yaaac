$(document).ready(function() {
    $(".yaaac_search_input").each(function() {
        $id_input = $(this).prev();
        var options = {
            serviceUrl: $id_input.attr("search_url"),
            onSelect: function(suggestion) {
                $id_input.val(suggestion.data);
            },
            params: {
                value_attr: $id_input.attr("value_attr")
            }
        };
        $input = $(this).autocomplete(options);
    });
});
