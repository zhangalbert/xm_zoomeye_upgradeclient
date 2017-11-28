// 公共变量区域
var url = '/ajax/firmware/list';
/*
'id': ins.id,
'log_level': ins.log_level,
'log_name': ins.log_name,
'log_class': ins.log_class,
'dao_name': ins.dao_name,
'file_type': ins.file_type,
'file_name': ins.file_name,
'file_url': ins.file_url,
'last_author': ins.last_author,
'last_date': ins.last_date,
'last_revision': ins.last_revision,
'last_action': ins.last_action,
'log_message': ins.log_message,
'created_date': ins.created_time.strftime('%Y-%m-%d'),
'created_time': ins.created_time.strftime('%H-%M-%S')
* */

// 入口
$(function () {
    // 点击搜索按钮
    $('#search_log_message').textbox({
        buttonText: '搜索',
        prompt: '搜一下, 又不会怀孕～',
        width: 300
    });
    // 右下方表格区
   $('#list-layout-body-bottom-table').datagrid({
        fit: true,
        method: 'GET',
        pageSize: 20,
        striped: false,
        remoteSort: false,
        url: url,
        rownumbers: false,
        pagination: true,
        fitColumns: true,
        singleSelect: true,
        checkOnSelect: true,
        selectOnCheck: true,
        columns:[[
            {
                field:'log_level',width:'5%',title:'日志级别',
                formatter: function(value,row,index){
                    return '<span class="text-'+value+'"><i class="fa fa-circle" aria-hidden="true"></i></span>';
                },align:'center'
            },
            {
                field:'log_class',width:'10%',title:'日志类名'
            },
            {
                field:'dao_name',width:'5%',title:'固件型号'
            },
            {
                field:'file_type',width:'5%',title:'型号类别'
            },
            {
                field:'log_message',width:'66%',title:'异常信息'
            },
            {
                field:'created_time',width:'%5',title:'异常时间',align:'right'
            }
        ]]
    });
    // 点击搜索事件
    $('#search_log_message').on('click', function () {
        var q_params = {},
            log_level = $('#search_log_level').combobox('getValue'),
            log_class = $('#search_log_class').combobox('getValue'),
            dao_name = $('#search_dao_name').combobox('getValue'),
            file_type = $('#search_file_type').combobox('getValue'),
            log_message = $('#search_log_message').combobox('getValue');
        if(log_level != ''){q_params['log_level'] = log_level;}
        if(log_class != ''){q_params['log_class'] = log_class;}
        if(dao_name != ''){q_params['dao_name'] = dao_name;}
        if(file_type != ''){q_params['file_type'] = file_type;}
        if(log_message != ''){q_params['log_message'] = log_message;}

        $('#list-layout-body-bottom-table').datagrid('load', q_params);
    });
});