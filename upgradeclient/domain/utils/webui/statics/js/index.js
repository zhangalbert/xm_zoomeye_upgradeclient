// 公共变量区域
var exception_trend_chart = null
    ,exception_nametype_chart = null
    ,exception_thread_chart = null
    ,exception_trend_chart_data = []
    ,exception_nametype_chart_data = []
    ,exception_thread_chart_data = [];


// 右侧实时异常列表
function realtime_ajax_exception_realtime(){
    var eurl = '/ajax/exception/realtime',
        data = {
            log_level: $('#log_level').combobox('getValue'),
            log_limit: $('#log_limit').combobox('getValue')
        };
    $.ajax({
        type: 'GET',
        url: eurl,
        data: data,
        dataType: 'json',
        success: function(data) {
            var html = '';
            for (var i = 0; i < data.length; i++) {
                var cur_ins = data[i];
                html = html + '<section>' +
                              '<span class="point-time text-'+cur_ins['log_level']+'">' +
                              '<i class="fa fa-circle-o" aria-hidden="true"></i></span>' +
                              '<time><span>'+cur_ins['created_date']+'</span><span>'+cur_ins['created_time'] +
                              '</span></time><aside><p class="things text-'+cur_ins['log_level']+' rtrim">' +
                              '<a href="/firmware/'+cur_ins['id']+'" target="_blank">'+cur_ins['log_message'] +
                              '</p></aside></section>';
            }
            $('#exception_realtime').html(html);
        }
    })
}

// 左下方固件异常趋势
function realtime_ajax_exception_trend(){
    var eurl = '/ajax/exception/excepts',
        data = {exp_during: $('#exp_during').combobox('getValue')};
    $.ajax({
        type: 'GET',
        url: eurl,
        data: data,
        dataType: 'json',
        success: function(data) {
            exception_trend_chart.series[0].setData(data);
        }
    })
}


// 左上线程异常趋势
function realtime_ajax_exception_thread() {
    var eurl = '/ajax/exception/threads',
        data = {};
    $.ajax({
        type: 'GET',
        url: eurl,
        data: data,
        dataType: 'json',
        success: function(data) {
            exception_thread_chart.series[0].setData(data);
        }
    })
}

// 左上型号异常趋势
function realtime_ajax_exception_nametype() {
    var eurl = '/ajax/exception/fmodels',
        data = {};
    $.ajax({
        type: 'GET',
        url: eurl,
        data: data,
        dataType: 'json',
        success: function(data) {
            exception_nametype_chart.series[0].setData(data);
        }
    })
}


// 入口
$(function(){
	// 图表实现自动伸缩
	$(window).resize(function(){
		exception_trend_chart & exception_trend_chart.reflow();
		exception_nametype_chart & exception_nametype_chart.reflow();
		exception_thread_chart & exception_thread_chart.reflow();
	});
	// 导航栏下拉菜单
	$('.upg-layout-header li.upg-dropdown').on('mouseover', function(){
		var left = $(this).offset().left- 100
			,top = 52;
		$('#user_profile').menu('show', {left: left, top: top, hideOnUnhover: true});
	});
	realtime_ajax_exception_realtime();
    setInterval(realtime_ajax_exception_realtime, 60000);

	// 固件异常趋势图
    exception_trend_chart = Highcharts.chart('exception_trend', {
        credits: {
            enabled: false
        },
        chart: {
            zoomType: 'x',
            spacing : [15, 15 , 0, 15]
        },
        title: {
            text: null
        },
        subtitle: {
            text: null
        },
        xAxis: {
            type: 'datetime',
            dateTimeLabelFormats: {
                millisecond: '%H:%M:%S.%L',
                second: '%H:%M:%S',
                minute: '%H:%M',
                hour: '%H:%M',
                day: '%m-%d',
                week: '%m-%d',
                month: '%Y-%m',
                year: '%Y'
            },
            labels: {
                formatter: function () {
                    var t = new Date(parseInt(this.value)*1000);
                    return t.getFullYear()+'-'+(t.getMonth()+1)+'-'+t.getDate();
                }
            }
        },
        tooltip: {
            dateTimeLabelFormats: {
                millisecond: '%H:%M:%S.%L',
                second: '%H:%M:%S',
                minute: '%H:%M',
                hour: '%H:%M',
                day: '%m-%d',
                week: '%m-%d',
                month: '%Y-%m',
                year: '%Y'
            },
            formatter: function () {
                var t = new Date(parseInt(this.x)*1000);
                return 'item: '+this.series.name+'<br/>'+'time: '
                       +' '
                       +t.getFullYear()+'-'+(t.getMonth()+1)+'-'+t.getDate()
                       +' '
                       +'[ '+this.y+' ]';
            }
        },
        yAxis: {
            title: {
                text: null
            }
        },
        legend: {
            enabled: false
        },
        plotOptions: {
            area: {
                fillColor: {
                    linearGradient: {
                        x1: 0,
                        y1: 0,
                        x2: 0,
                        y2: 1
                    },
                    stops: [
                        [0, Highcharts.getOptions().colors[0]],
                        [1, Highcharts.Color(Highcharts.getOptions().colors[0]).setOpacity(0).get('rgba')]
                    ]
                },
                marker: {
                    radius: 2
                },
                lineWidth: 1,
                states: {
                    hover: {
                        lineWidth: 1
                    }
                },
                threshold: null
            }
        },
        series: [{
            type: 'area',
            name: '固件异常趋势',
            data: exception_trend_chart_data
        }]
    });
    realtime_ajax_exception_trend();
    setInterval(realtime_ajax_exception_trend, 60000);

	// 类型异常趋势图
	$('#exception_nametype').highcharts({
	    credits: {
	        enabled: false
	    },
	    chart: {
	        plotBackgroundColor: null,
	        plotBorderWidth: null,
	        plotShadow: false,
	        spacing : [0, 15 , 0, 0]
	    },
	    title: {
	        floating: true,
	        text: null
	    },
	    tooltip: {
	        pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
	    },
	    plotOptions: {
	        pie: {
	            allowPointSelect: false,
	            cursor: 'pointer',
	            dataLabels: {
	                enabled: true,
	                distance: -10,
	                style: {
	                    fontWeight: 'bold',
	                    color: 'white',
	                    textShadow: '0px 1px 2px black'
	                },
	                format: '{point.name}'
	            },
	            point: {
	                events: {
	                    mouseOver: function(e) {
	                        exception_nametype_chart.setTitle({
	                            text: e.target.y + ' %'
	                        });
	                    }
	                }
	            },
	        }
	    },
	    series: [{
	        type: 'pie',
	        innerSize: '95%',
	        name: '固件型号异常占比',
	        data: [
	            ['IPC_General',   45.0],
	            ['IPC_OEM',       5.0],
	            ['DVR_General',       10.0],
	            ['DVR_OEM',    35.0],
	            ['NVR_General', 30.2],
	            ['NVR_OEM', 5.0]
	        ]
	    }]
	}, function(c) {
	    // 环形图圆心
	    var centerY = c.series[0].center[1],
	        titleHeight = parseInt(c.title.styles.fontSize);
	    c.setTitle({
	        y:centerY + titleHeight/2
	    });
	    exception_nametype_chart = c;
	});
	realtime_ajax_exception_nametype();
	setInterval(realtime_ajax_exception_nametype, 60000);

    // 线程异常趋势图
    $('#exception_thread').highcharts({
	    credits: {
	        enabled: false
	    },
	    chart: {
	        plotBackgroundColor: null,
	        plotBorderWidth: null,
	        plotShadow: false,
	        spacing : [0, 15 , 0, 0]
	    },
	    title: {
	        floating: true,
	        text: null
	    },
	    tooltip: {
	        pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
	    },
	    plotOptions: {
	        pie: {
	            allowPointSelect: false,
	            cursor: 'pointer',
	            dataLabels: {
	                enabled: true,
	                distance: -10,
	                style: {
	                    fontWeight: 'bold',
	                    color: 'white',
	                    textShadow: '0px 1px 2px black'
	                },
	                format: '{point.name}'
	            },
	            point: {
	                events: {
	                    mouseOver: function(e) {
	                        exception_thread_chart.setTitle({
	                            text: e.target.y + ' %'
	                        });
	                    }
	                }
	            },
	        }
	    },
	    series: [{
	        type: 'pie',
	        innerSize: '95%',
	        name: '线程异常分布',
	        data: [
	            ['CheckService',   0.0],
	            ['DownloadService',       50.0],
	            ['UploadService',       0.0],
	            ['AlertService',    0.0],
	            ['FirmwareHandler', 25.0],
	            ['ReleaseNoteHandler', 25.0]
	        ]
	    }]
	}, function(c) {
	    // 环形图圆心
	    var centerY = c.series[0].center[1],
	        titleHeight = parseInt(c.title.styles.fontSize);
	    c.setTitle({
	        y:centerY + titleHeight/2
	    });
	    exception_thread_chart = c;
	});
    realtime_ajax_exception_thread();
    setInterval(realtime_ajax_exception_thread, 60000);
});
