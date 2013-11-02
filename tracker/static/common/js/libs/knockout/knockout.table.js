ko.bindingHandlers.sort = {
    //binded to viewModel.sort, check that field is exists
    init: function(element, valueAccessor, allBindingsAccessor, viewModel) {
        var baseval = ko.utils.unwrapObservable(valueAccessor());
        var element = $(element);

        function getField(val) {
            if (val[0] == '-') return val.slice(1);
            return val;
        }
        function setClasses(newval) {
            var asc = true;
            if (newval[0] == '-') {
                newval = newval.slice(1);
                asc = false;
            }
            if (newval == baseval && asc && !element.hasClass("asc"))
                element.removeClass("desc").addClass("asc");
            else if (newval == baseval && !asc && !element.hasClass("desc"))
                element.removeClass("asc").addClass("desc");
            else
                element.removeClass("asc desc");
        }
        element.addClass("sortable").live("click", function () {
            var curval = viewModel.sort();
            var field = getField(curval);

            if (baseval == field) {
                if (curval[0] == '-') viewModel.sort(baseval);
                else viewModel.sort('-' + baseval);
            }
            else {
                viewModel.sort(baseval);
            }
        });
        viewModel.sort.subscribe(function (val) {
            setClasses(val);
        })

        var curval = viewModel.sort();
        setClasses(curval);
    }
}

ko.bindingHandlers.listFilter = {
    //for filters
    //sample: data-bind="listFilter: 'all', value: category",
    // if value not exists, binds to viewModel.flt

    init: function(element, valueAccessor, allBindingsAccessor, viewModel) {
        var baseval = ko.utils.unwrapObservable(valueAccessor());
        var element = $(element);

        var value = null;
        if (allBindingsAccessor().hasOwnProperty('value'))
            value = allBindingsAccessor().value;
        else
            value = viewModel.flt;

        function setClasses(newval) {
            if (newval == baseval && !element.hasClass("current"))
                element.addClass("current");
            else
                element.removeClass("current");
        }
        element.bind("click", function () {
            value(baseval);
        });
        value.subscribe(function (val) {
            setClasses(val);
        })

        var curval = value();
        setClasses(curval);
    }
}