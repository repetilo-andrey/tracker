var stop = function(){
    clearTimeout(interval);
    interval = null;
};

function Tickets() {
    var self = this;

    self.projects = ko.observableArray();
    self.tickets = ko.observableArray();
    self.current_ticket_id = null;
    self.project_name = 'select';

    self.get_projects = function() {
        rpc('get_projects', [], function(data) {
            $.each(data.projects, function(i, v){
                self.projects.push(v)
            })
        });
    };

    self.get_tickets = function() {
        rpc('get_tickets', [], function(data) {
            $.each(data.tickets, function(i, v){
                self.tickets.push(v)
            })
        });
    };

    self.get_projects();
    self.get_tickets();

    self.start_timer = function() {
        var ticket_id = $(this).attr('id');
        var stop = $('#'+ticket_id+' .stop-timing');

        rpc('create_time_period', [ticket_id, 0], function(data) {});

        $('.start-button').hide();
        $('#calculating_time').hide();
        stop.show();
        self.current_ticket_id = ticket_id;
        self.timerFunc();
        window.onbeforeunload = function () {
            return ('Are you sure you stopped logging of time?')
        };
        interval = setInterval(self.timerFunc, 1000);
    };

    self.stop_timer = function() {
        var ticket_id = self.current_ticket_id;
        rpc('create_time_period', [ticket_id, 1], function(data) {});
        $('.stop-timing').hide();
        $('.start-button').show();
        $('#calculating_time').show();
        window.onbeforeunload = null;
        stop();
    };

    self.timerFunc = function(){
        var ticket_id = self.current_ticket_id;

        var hh = $('#'+ticket_id+' .hours').text();
        var mm = $('#'+ticket_id+' .minutes').text();
        var ss = $('#'+ticket_id+' .secundes').text();

        if(ss == 59){
            if(mm == 59){
                mm = -1;
                hh++;
            }
            ss = -1;
            mm++;

            rpc('show_logged_time', [$('#'+ticket_id+' .time-logged').text()], function(data) {
                $('#'+ticket_id+' .time-logged').text(data.html)
            });
        }
        ss++;

        $('#'+ticket_id+' .hours').text(hh);
        $('#'+ticket_id+' .minutes').text(mm);
        $('#'+ticket_id+' .secundes').text(ss);
    };

    self.show_new_project = function() {
        $('.new-project-name').css('display','block');
        $('#create_ticket_form select').css('display','none');
        $('#create_ticket_form p').css('display','none');
        self.project_name = 'input'
    };

    self.create_new_ticket = function() {
        $('.error').remove();
        var new_project = 0;
        var name = $('#ticket_name');
        if (self.project_name =='select')
            var project_value = $('select','#create_ticket_form').find(":selected").text();
        else{
            var project_name = $('#project_name');
            var project_value = project_name.val();
            new_project = 1;
        }
        var value = name.val();
        if (value == '')
            name.after("<p class='error'>Name can not be empty.</p>");
        else if (project_value == '')
            project_name.after("<p class='error'>Name can not be empty.</p>");
        else{
            rpc('create_ticket', [project_value, value, new_project], function(data) {
                if (data.ticket_error)
                    name.after("<p class='error'>"+data.error+"</p>");
                else if (data.project_error)
                    project_name.after("<p class='error'>"+data.error+"</p>");
                else{
                    $('input','#create_ticket_form').val('');
                    $('#create_ticket_form').modal('hide');
                    self.tickets.push(data.ticket_data)
                }
            });
        }
    };

    self.close_open_ticket = function() {
        var self = $(this);
        rpc('close_open_ticket', [$(this).attr('id')], function() {
            var tr = $('#'+self.attr('id'), 'tbody');
            tr.hide("slow", function(){ tr.remove(); });
        });
    };
}

ko.applyBindings(new Tickets());
