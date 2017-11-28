$(function () {
    // 导航栏下拉菜单
    $('.upg-layout-header li.upg-dropdown').on('mouseover', function(){
        var left = $(this).offset().left- 100
            ,top = 52;
        $('#user_profile').menu('show', {left: left, top: top, hideOnUnhover: true});
    });
});
