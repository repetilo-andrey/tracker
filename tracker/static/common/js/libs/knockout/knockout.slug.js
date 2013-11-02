ko.bindingHandlers.slugify = {
    update: function(element, valueAccessor, allBindingsAccessor) {
        var set_alias = valueAccessor(), allBindings = allBindingsAccessor();
        var val = allBindings.value();
        set_alias(URLify(val));
    }
};