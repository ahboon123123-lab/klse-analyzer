// 发送短信重置时间
var mobileResetTime = 60;

$(document).ready(function() {
	// 默认禁用重新发送按钮
	resetSend();
	
	// 提交表单
	$('#btn_reg').click(function() {
		// 验证码
		var verfication = $.trim($('#email').val());
		//alert(verfication);
		if (verfication == '') {
			$.simplyToast('Please Enter the Email!', 'warning', {'offset':{'amount':20}});
			return false;
		}
		validEmailNew();
		return false;
	});
	
	// 重新发送手机验证码
	$('#reSend').click(function() {
		// 禁用发送按钮
		resetSend();
		
//		$.post('url', {'mobile':mobile}, function(data) {
//			
//		});
	});
});
	
function resetSend() {
	
}
/**
 * 
 * @param {Object} code
 * @return {TypeName} 
 */
function valcode(code,num){
	var codeV = -1;
	if($.trim(code)!=''){
		$.post("validCode",{validcode:code},function(data){
			codeV = data;
			//alert(codeV=='1');
			switch(data){
				case '0':$.simplyToast('验证码输入错误!', 'warning', {'offset':{'amount':20}});break;
				case '1':;break;
				case '2':$.simplyToast('验证码输入错误!', 'warning', {'offset':{'amount':20}});break;
			}
			if(codeV=='1'){
				return true;
			}else{
				$('#verfication').val('');
				return false;
			}
		})
	}
}

/**
 * 重新发送
 */
function resetCode(mobile){
	resetSend();
	$.post("sendValidCode",{mobile:mobile},function (data){
		switch(data){
		case 1:break;
		case 2:$.simplyToast('验证次数过多，请稍后重试!', 'warning', {'offset':{'amount':20}});break;
		case 3:$.simplyToast('验证码发送失败!', 'warning', {'offset':{'amount':20}});break;
		}
	})
}
/**
 * 验证手机号
 */
var userExist=-2;
function validMobile(mobile,num) {
   
	if (/^1[3|4|5|7|8]\d{9}$/.test($.trim(mobile))) {
		//alert(mobile+"--");
		$.post("validUser",{mobile:mobile},function(data){
			//alert(data);
			if(data==-1){
				//alert("验证出错，请重试");
				userExist =-1;
				$.simplyToast('手机号码不正确!', 'warning', {'offset':{'amount':20}});
				$("#mobile").val('');
			}
			if(data==0){
				userExist = 0;
				$.simplyToast('手机号码不存在，请重新錄入!', '提示', {'offset':{'amount':20}});
				$("#mobile").val('');
			}
			if(data>0){
				userExist = data;
				if(num==1){
					$('#form').submit();
				}
			}
		});
	}else{
		$.simplyToast('手机号码不正确!', 'warning', {'offset':{'amount':20}});
		return false;
	}
}
/**
 * 验证邮箱
 * @return
 */
function validEmail(){
	 var email = $.trim($('#email').val());
	   if (email != "") {  
	      var reg = /^\w+((-\w+)|(\.\w+))*\@[A-Za-z0-9]+((\.|-)[A-Za-z0-9]+)*\.[A-Za-z0-9]+$/;  
	 	  isok= reg.test(email );  
	 	  if (!isok) {  
	            alert("Please enter your email address in the format!");
	              $('#email').focus();
	              return false;  
	     		 }
	 	  $.post("mobileHz/validEmail",{email:email},function(data){
				//alert(data);
				if(data==-28){
					//alert("验证出错，请重试");
					userExist =-1;
					$.simplyToast('Email is wrong!', 'warning', {'offset':{'amount':20}});
					$("#email").val('');
				}
				if(data==-11){
					userExist = 0;
					$.simplyToast('Email is exist,please enter again!', 'info', {'offset':{'amount':20}});
					$("#email").val('');
				}
				if(data>0){
					userExist = data;
					$('#form').submit();
				}
			});
	      }
}
/**
 * 验证邮箱
 * @return
 */
function validEmailNew(){
	 var email = $.trim($('#email').val());
	 var username = $.trim($('#username').val());
	   if (email != "") {  
	      var reg = /^\w+((-\w+)|(\.\w+))*\@[A-Za-z0-9]+((\.|-)[A-Za-z0-9]+)*\.[A-Za-z0-9]+$/;  
	 	  isok= reg.test(email );  
	 	  if (!isok) {  
	            alert("Please enter your email address in the format!");
	              $('#email').focus();
	              return false;  
	     		 }
	 	  $.post("mobileHz/validEmail",{email:email,username:username},function(data){
				//alert(data);
				if(data==-28){
					//alert("验证出错，请重试");
					userExist =-1;
					$.simplyToast('Email is wrong!', 'warning', {'offset':{'amount':20}});
					$("#email").val('');
				}
				if(data==-11){
					userExist = 0;
					$.simplyToast('Email is exist,please enter again!', 'info', {'offset':{'amount':20}});
					$("#email").val('');
				}
				if(data>0){
					userExist = data;
					$('#form').submit();
				}
			});
	      }
}
function tjOk(){
	if(validMobile($("#mobile").val())){
		document.forms[0].submit();
		return true;
	}else{
		return false;
	}
}
