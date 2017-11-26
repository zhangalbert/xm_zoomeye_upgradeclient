$(function(){
	var exception_trend_chart = null
		,exception_nametype_chart = null
		,exception_thread_chart = null;
	// $(window).resize(function(){
	// 	exception_trend_chart & exception_trend_chart.reflow();
	// 	exception_nametype_chart & exception_nametype_chart.reflow();
	// 	exception_thread_chart & exception_thread_chart.reflow();
	// })
	// 导航栏下拉菜单
	$('.upg-layout-header li.upg-dropdown').on('mouseover', function(){
		var left = $(this).offset().left- 100
			,top = 52;
		$('#user_profile').menu('show', {left: left, top: top, hideOnUnhover: true});
	});
	// 右侧实时异常列表
    setInterval(function realtime_ajax_exception_realtime(){
        $.ajax({
            type: 'GET',
            url: '/ajax/exception/realtime',
            data: {},
            dataType: 'json',
            success: function(data) {
                var html = '';
                for (var i = 0; i < data.length; i++) {
                    var cur_ins = data[i];
                    html = html + '<section pk="'+cur_ins['id']+'">' +
                                  '<span class="point-time text-'+cur_ins['log_level']+'">' +
                                  '<i class="fa fa-circle-o" aria-hidden="true"></i></span>' +
                                  '<time><span>'+cur_ins['created_date']+'</span><span>'+cur_ins['created_time'] +
                                  '</span></time><aside><p class="things text-'+cur_ins['log_level']+' rtrim">' +
                                  cur_ins['log_message']+'</p></aside></section>';
                }
                $('#exception_realtime').html(html);
            }
        })
    }, 5000);

	// 固件异常趋势图
	$.getJSON('/ajax/exception/excepts', function (data) {
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
                        return t.getHours()+':'+t.getMinutes();
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
                           +t.getFullYear()+'-'+t.getMonth()+'-'+t.getDate()
                           +' '
                           +t.getHours()+':'+t.getMinutes()+t.getSeconds()
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
	            data: data
	        }]
	    });
	});
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
	        name: '固件型号异常占比',
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
});
