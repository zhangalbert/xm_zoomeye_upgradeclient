$(function(){
	var exception_trend_chart = null
		,exception_nametype_chart = null
		,exception_thread_chart = null;
	$(window).resize(function(){
		exception_trend_chart & exception_trend_chart.reflow();
		exception_nametype_chart & exception_nametype_chart.reflow();
		exception_thread_chart & exception_thread_chart.reflow();
	})
	// 导航栏下拉菜单
	$('.upg-layout-header li.upg-dropdown').on('mouseover', function(){
		var left = $(this).offset().left- 100
			,top = 52;
		$('#user_profile').menu('show', {left: left, top: top, hideOnUnhover: true});
	});
	// 固件异常趋势图
	$.getJSON('https://data.jianshukeji.com/jsonp?filename=json/usdeur.json&callback=?', function (data) {
	    exception_trend_chart = Highcharts.chart('exception_trend', {
	    		credits: { 
	    			enabled: false
	    		},
	        chart: {
	            zoomType: 'x',
	            spacing : [15, 15 , 0, 15]
	        },
	        title: {
	            text: null,
	        },
	        subtitle: {
	            text: null,
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
	            }
	        },
	        tooltip: {
	            dateTimeLabelFormats: {
	                millisecond: '%H:%M:%S.%L',
	                second: '%H:%M:%S',
	                minute: '%H:%M',
	                hour: '%H:%M',
	                day: '%Y-%m-%d',
	                week: '%m-%d',
	                month: '%Y-%m',
	                year: '%Y'
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
	            name: '美元兑欧元',
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
	            ['IPC_OEM',       12.0],
	            ['DVR_General',       26.8],
	            ['DVR_OEM',    8.5],
	            ['NVR_General', 30.2],
	            ['NVR_OEM', 0.7]
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
	            ['CheckService',   45.0],
	            ['DownloadService',       12.0],
	            ['UploadService',       26.8],
	            ['AlertService',    8.5],
	            ['FirmwareHandler', 30.2],
	            ['ReleaseNoteHandler', 0.7]
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
