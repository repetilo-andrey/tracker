function Archive() {
    var self = this;

    self.projects = ko.observableArray();

    rpc('get_archived_tickets', [], function(data) {
        $.each(data.projects, function(i, v){
            self.projects.push(v)
        })
    });

    self.close_open_ticket = function() {
        var self = $(this);
        rpc('close_open_ticket', [$(this).attr('id')], function() {
            var tr = $('#'+self.attr('id'), 'tbody');
            tr.hide("slow", function(){ tr.remove(); });
        });
    };
}

ko.applyBindings(new Archive());