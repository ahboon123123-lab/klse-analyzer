/**
 * 掌中宝用户激活验证
 */
$(document).ready(function() {
	
	// 页面语言配置
	var language = {en : {
							userActivate : 'User activate',
							username : 'Username: ',
							email : 'Email: ',
							formmsg : 'Please confirm your email address!',
							submitbtn : 'Submit'
						  },
			        cn : {
							  userActivate : '用户激活',
							  username : '用户名: ',
							  email : '电子邮箱: ',
							  formmsg : '请确认您的电子邮箱地址!',
							  submitbtn : '提交'
						 }};
	
	// 浏览器语言(默认中文)
	var lan = true;
	var isIe = $.browser.msie;
	if ((isIe && window.navigator.userLanguage.toLowerCase() == 'zh-cn') || window.navigator.language.toLowerCase() == 'zh-cn' ) {
		document.title = '用户激活';
		$('#userActivate_text').html(language.cn.userActivate);
		$('#username_text').html(language.cn.username);
		$('#email_text').html(language.cn.email);
		$('#form_msg').html(language.cn.formmsg);
		$('#submitBtn').val(language.cn.submitbtn);
	} else {
		$('#userActivate_text').html(language.en.userActivate);
		$('#username_text').html(language.en.username);
		$('#email_text').html(language.en.email);
		$('#form_msg').html(language.en.formmsg);
		$('#submitBtn').val(language.en.submitbtn);
		lan = false;
	}
	
	// activate_form submit
	$('#submitBtn').click(function() {
		var username = $.trim($('#username').val());
		var email = $.trim($('#email').val());
		
		if (email == '') {
			if (lan) {
				$('#form_msg').html('<span class="error">请输入您的电子邮箱!</span>');
			} else {
				$('#form_msg').html('<span class="error">Please input your email address!</span>');
			}
			return false;
		}
		
		if (!/^(?:\w+\.?)*\w+@(?:\w+\.)*\w+$/.test(email)) {
			if (lan) {
				$('#form_msg').html('<span class="error">电子邮箱格式不正确!</span>');
			} else {
				$('#form_msg').html('<span class="error">email address do not match!</span>');
			}
			return false;
		}
		
		$('#activateResult').show();
		
		// loading
		if (lan) {
			$('#activateResult').html('<div class="loading"><img src="images/loading.gif" />激活邮件正在发送中,请稍等...</div>');
		} else {
			$('#activateResult').html('<div class="loading"><img src="images/loading.gif" />Please waiting...</div>');
		}
		
		// 禁用提交按钮
		$('#submitBtn').attr('disabled', true);
		
		// post activate message
		$.ajax({
			url: 'mobile/activate',
			method: 'post',
			data: {
				'username' : username,
				'email' : email
			},
			cache: false,
			dataType: 'html',
			success: function(data) {
				if (data == '-15') {
					// 启用提交按钮
					$('#submitBtn').attr('disabled', false);
					
					// 发送失败
					if (lan) {
						$('#activateResult').html('<div class="failed">' +
							                  	    '<p><img src="images/register-error.gif" />激活邮件发送失败,请尝试重新发送!</p>' +
											      '</div>');
					} else {
						$('#activateResult').html('<div class="failed">' +
							                 	    '<p><img src="images/register-error.gif" />The email send failed, please retry!</p>' +
											      '</div>');
					}
				} else if (data == '-11') {
					// 该邮箱已存在
					$('#submitBtn').attr('disabled', false);
					
					// 发送失败
					if (lan) {
						$('#form_msg').html('<div class="error">该邮箱已存在</div>');
						$('#activateResult').html('<div class="failed">' +
							                  	    '<p><img src="images/register-error.gif" />激活邮件发送失败,该邮箱已存在,请更换后重试!</p>' +
											      '</div>');
					} else {
						$('#form_msg').html('<div class="error">The email address was already exists</div>');
						$('#activateResult').html('<div class="failed">' +
							                 	    '<p><img src="images/register-error.gif" />The email send failed, email address was already exists!</p>' +
											      '</div>');
					}
				} else if (data == '103') {
					// 发送成功
					if (lan) {
						$('#activateResult').html('<div class="success">' +
													'<p><img src="images/register-ok.gif" />激活邮件发送成功,请您马上激活!</p>' +
													'<p class="confirm_msg">如您长时间未收到邮件,请尝试重新发送!</p>' +
												  '</div>');
					} else {
						$('#activateResult').html('<div class="success">' +
													'<p><img src="images/register-ok.gif" />The email send success, please activate your account!</p>' +
													'<p class="confirm_msg">If you are not a long time to receive e-mail, please re-send!</p>' +
												  '</div>');
					}
				}
			},
			error: function() {
				// 发送失败
				if (lan) {
					$('#activateResult').html('<div class="failed">' +
						                  	       '<p><img src="images/register-error.gif" />激活邮件发送失败,请尝试重新发送!</p>' +
										      '</div>');
				} else {
					$('#activateResult').html('<div class="failed">' +
						                  	       '<p><img src="images/register-error.gif" />The email send failed, please retry!</p>' +
										      '</div>');
				}
			}
		});
	});
});
