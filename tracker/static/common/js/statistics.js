MONTHS_IN_YEAR = [
    { value: 'Current month' },
    { id: 1, value: 'January', days: 31},
    { id: 2, value: 'February', days: 28},
    { id: 3, value: 'March', days: 31},
    { id: 4, value: 'April', days: 30},
    { id: 5, value: 'May', days: 31},
    { id: 6, value: 'June', days: 30},
    { id: 7, value: 'July', days: 31},
    { id: 8, value: 'August', days: 31},
    { id: 9, value: 'September', days: 30},
    { id: 10, value: 'October', days: 31},
    { id: 11, value: 'November', days: 30},
    { id: 12, value: 'December', days: 31}
];

var previousPoint = null;

// Hover effect
$("#placeholder").bind("plothover", function (event, pos, item) {
    if (item) {
        if (previousPoint != item.dataIndex) {
            previousPoint = item.dataIndex;
            $("#tooltip").remove();
            var value = 'Day ' + item.datapoint[0] + '<br>' + get_time(item.datapoint[1]);
            $('<div id="tooltip">' + value + '</div>').css({
                position: 'absolute',
                display: 'none',
                top: item.pageY - 65,
                left: item.pageX + 5,
                border: '1px solid #fdd',
                padding: '5px',
                'background-color': '#fee',
                opacity: 0.90
            }).appendTo("body").fadeIn(200);
        }
    } else {
        $('#tooltip').remove();
        previousPoint = null;
    }
});

function get_time(val) {
    var number = val.toString();
    var s = number.slice(number.length - 2);
    number = number.slice(0, -2);
    var m = number.slice(number.length - 2);
    number = number.slice(0, -2);
    var h = number.slice(number.length - 2);
    if (h)
        return h + ':' + m + ':' + s;
    else if (m)
        return '00:' + m + ':' + s;
    else
        return '00:00:' + s;
}

function Statistics() {
    var self = this;

    self.days = ko.observableArray();

    self.years = ko.observableArray();
    self.year = ko.observable();

    self.month = ko.observable();
    self.months_in_year = ko.observableArray(MONTHS_IN_YEAR);

    self.time_for_month = ko.observable('');
    self.time_by_tickets = ko.observableArray();

    self.all_data = [[]];
    self.ticks = [];

    rpc('get_month_and_years', [], function(data) {
        self.years(data.years);
        self.year(data.year);

        self.month(data.month);
        MONTHS_IN_YEAR[0]['id'] = self.month();
        MONTHS_IN_YEAR[0]['days'] = MONTHS_IN_YEAR[self.month()].days;
    });

    self.get_stat_by_day = function(month, cur_year) {
        for (var i = 0; i < self.years().length; i++){
            if(self.years()[i].id == cur_year)
                var year = self.years()[i].value
        }
        if(month){
            rpc('get_day_stat', [parseInt(month), parseInt(year)], function(data) {
                self.ticks = [];
                self.all_data = [[]];
                self.days([]);
                self.time_by_tickets([]);
                self.time_for_month(data.month_time);
                var times = [];
                var work_days = [];

                if (Object.keys(data.stat_by_day).length != 0){
                    var days = MONTHS_IN_YEAR[self.month()].days;
                    if (new Date(year, 1, 29).getMonth() == 1)  //  if leap year. then 29 days in February
                        days = 29;

                    for (var i = 1; i <= days; i++){
                        self.ticks.push(i)
                    }

                    $.each(data.stat_by_ticket, function(i, v){
                        self.time_by_tickets.push(v)
                    });

                    $.each(data.stat_by_day, function(i, v){
                        self.days.push(v);

                        var time = v.total_time.split(/:/);
                        times.push(time[0] + time[1] + time[2]);
                        work_days.push(v.day_number)
                    });

                    $.each(self.ticks, function(i, v){
                        if ($.inArray(v, work_days) > -1){
                            self.all_data[0].push([v, times[work_days.indexOf(v)]])
                        }
                        else{
                            self.all_data[0].push([v, '000'])
                        }
                    });

                    var plot_format = {
                        points: {show: true},
                        series: {
                            lines: {show: true, lineWidth: 2}
                        },
                        grid: { hoverable: true},
                        xaxis: {
                            ticks: self.ticks
                        },
                        yaxis: {
                            tickFormatter: function(val) {
                                return get_time(val)
                            }
                        }
                    };
                    $('.base').remove();  // remove canvas, remains after info about no data for month
                    $.plot($("#placeholder"), self.all_data, plot_format);
                }
                else{
                    // add canvas if in default month no data
                    if (!$('.base')[0])
                        $('#placeholder').html('<canvas class="base" width="600" height="401"></canvas>');
                    var canvas = $('.base')[0];
                    var ctx = canvas.getContext("2d");

                    ctx.setTransform(1, 0, 0, 1, 0, 0);
                    ctx.clearRect(0, 0, canvas.width, canvas.height);
                    ctx.restore();
                    $('.tickLabels').remove();

                    var textString = "No data for " + MONTHS_IN_YEAR[self.month()].value;
                    ctx.font = 'bold 30px sans-serif';
                    ctx.strokeText(textString, 150, 200);
                }
            });
        }
    };

    self.month.subscribe(function(value) {
        self.get_stat_by_day(value, self.year())
    });
    self.year.subscribe(function(value) {
        self.get_stat_by_day(self.month(), value)
    });
}

ko.applyBindings(new Statistics());


