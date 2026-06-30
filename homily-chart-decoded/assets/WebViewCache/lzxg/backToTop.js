/**
 * 返回页面顶部
 */
$(document).ready(function() {
    // 是否是ie6
    var isIe6 = $.browser.msie && $.browser.version == '6.0';

    var style = '<style type="text/css">' +
                    '#backToTop {' +
                        'display: none;' +
                        'width: 48px;' +
                        'height: 49px;' +
                        'cursor: pointer;' +
                        'position: fixed;' +
                        'bottom: 80px;' +
                        'right: 100px;' +
                        'background: url(\'http://sg.legu168.com/kaisite/images/backToTop.png\') no-repeat 0px 0px;' +
                    '}' +
                    '#backToTop:hover {' +
                    	'background: url(\'http://sg.legu168.com/kaisite/images/backToTop.png\') no-repeat -48px 0px;' +
                    '}' +
                '</style>';
    var backToTop = '<div id="backToTop"></div>';
    $('body').append(style);
    $('body').append(backToTop);

    // ie6不可以使用fixed
    if (isIe6) {
        $('#backToTop').css('position', 'absolute');
    }

    $(window).scroll(function() {
        if ($(window).scrollTop() > 150) {
            if (isIe6) {
                $('#backToTop').hide();
                window.setTimeout(function() {
                	$('#backToTop').show();
                }, 600);
            } else {
                $('#backToTop').fadeIn(800);
            }
        } else {
            $('#backToTop').fadeOut(400);
        }
    });

    // 返回顶部
    $('#backToTop').click(function() {
        $('html, body').animate({scrollTop: 0}, 600);
    });
});
