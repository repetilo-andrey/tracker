moment.lang('ru');

ko.bindingHandlers.dateString = {
    update: function(element, valueAccessor, allBindingsAccessor, viewModel) {
        var value = valueAccessor();
        var valueUnwrapped = ko.utils.unwrapObservable(value);
        if(valueUnwrapped) {
            $(element).text(moment(valueUnwrapped).format('LL'));
        }
    }
};