$(document).ready(function() {
    $(".yaaac_search_input").each(function() {
        $id_input = $(this).prev();
        var options = {
            serviceUrl: $id_input.attr("search_url")
        };
        $input = $(this).autocomplete(options);
    });
});
