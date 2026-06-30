var dwidth;
var state; //根据状态判断是否转动大转盘
var position; //确定转动到什么位置
var code1 = " ",
	code2 = " ",
	code3 = " "; //转动出的股票代码最少：没有，最多三个
var typeList; //确定是转金币还是牛股
var coin; //转到金币的个数
var device = 3; // 1: android, 2: ios, 3: pc
var selectType = "7";//选择转的类型
var isTurn=true;

var turnplate = {
	restaraunts: [], //大转盘奖品名称
	colors: [], //大转盘奖品区块对应背景颜色
	outsideRadius: 192, //大转盘外圆的半径
	textRadius: 155, //大转盘奖品位置距离圆心的距离
	insideRadius: 68, //大转盘内圆的半径
	startAngle: 0, //开始角度
	bRotate: false //false:停止;ture:旋转
};
$(document).ready(function() {
	// 国际化
	globalI18n();

	//动态添加大转盘的奖品与奖品区域背景颜色
	turnplate.restaraunts = [languages.turnplateText1, languages.turnplateText7, languages.turnplateText2, languages.turnplateText1, languages.turnplateText7, languages.turnplateText2];
	turnplate.colors = ["#FF99CB","#FFFF95","#CC94FF"];
	var rotateTimeOut = function() {
		$('#wheelcanvas').rotate({
			angle: 0, //起始角度
			animateTo: 2160, //结束角度
			duration: 2000, //转动时间
			callback: function() { //回调函数
				alert(languages.alertText1);
			}
		});
	};
	//旋转转盘 item:奖品位置; txt：提示语;
	var rotateFn = function(item, txt) {
		var angles = item * (360 / turnplate.restaraunts.length) - (360 / (turnplate.restaraunts.length * 2));
		if(angles < 270) {
			angles = 270 - angles;
		} else {
			angles = 360 - angles + 270;
		}
		var dur = 2000;
		var zpto=900;
		if (txt == '')
		{
			dur = 2000*15;
			zpto=900*15;
		}
		$('#wheelcanvas').stopRotate();
		$('#wheelcanvas').rotate({
			angle: 0,
			animateTo: angles + zpto,
			duration: dur,
			callback: function() {
				//alert("您好，您转到了："+txt);		//弹出大转盘最终结果的对话框
				isTurn=true;
				$('#texiao').show();

				$(function() {
					$('.container1').css({
						width: $('.main').width(),
						height: $('.main').height()
					});
					anim();
				});

				function anim() {
					$('#anim').show();
					$('#anim').addClass('animated wobble');
					console.log('anim1');
					$('#anim').one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend', function() {
					console.log('anim2');
						txt = " ";
						if(item!=-1){
							var option = {
									title: languages.titleText,
									btn: parseInt("0010", 2),
									onCancel: function() {
										index = 0;
										$('.container1').hide();
										$('#anim').hide();
										$('#anim').removeClass();
									}
								}
						}else{//网络异常，添加金币失败
							var option = {
									title:languages.errorTitle,
									btn: parseInt("0010", 2),
									onCancel: function() {
										index = 0;
										$('.container1').hide();
										$('#anim').hide();
										$('#anim').removeClass();
									}
								}
						}
						
						window.wxc.xcConfirm(txt, "info", option);
					});
				}

				turnplate.bRotate = !turnplate.bRotate; //false:停止;ture:旋转，默认值是false
			}
		});
	};

	// 判断Android和Ios
	androidIos();

	// 判断能否打开当前页面
	canOpenPage();

	// 加载转股记录数据
	loadZhuanGuRecord();
	
//选股的点击事件
	$('.pointer').click(function() {
		if(!isTurn){
			return;
		}
		isTurn=false;
		var cs;
		// 获取字符串
		var path = "";
		if(device == 2) {//与IOS的交互
			SelectedStockAction("SelectedStockAction");
			cs=jsobjectmodel.getZhuanGuParams();
			path = "getxgResult_new.shop?"+encodeURI(cs)+"&type="+selectType;
		} else if (device == 1) {//与Android的交互
			cs = window.wxc.getPlateRoateState();
			path = "getxgResult_new.shop?"+encodeURI(cs)+"&type="+selectType;
		} else {
			cs = "jwcode=7c4f52d2f8137c637d750d6e273367a69886ecd782e17d84&name=NDXS&type=1&zbid=76&yzcode=129e7e866fc1b8d6a6b86deb8a623f7b76c8a0fd241050127ccfe675643ab243";
			path = "getxgResult_new.shop?"+encodeURI(cs);
		}
		
		coin = 0;
		code1 = " ",
		code2 = " ",
		code3 = " ";

		//先判断还有没有转股次数  surplucounts
		//没有的话，直接提示
		//alert();
		//alert($('#surplucounts').text());
		if($('#surplucounts').text()!='0' && $('#t_surplucounts').text().indexOf("0")<0){
			rotateFn(1, '');
		}
		
		// 请求数据
		$.ajax({
			url: path,
			dataType: "jsonp",
			jsonpCallback: "callback", //需要的回调函数
			success: function(result) {
				state = result.sate;
				position = result.result;
				typeList = result.type;
				coin = result.coin;
				
				if(typeList == "2") {
					var stock = result.stock;
//					alert(stock.length);
					if(stock.length == "1") {
						code1 = stock[0];
					} else if(stock.length == "2") {
						code1 = stock[0];
						code2 = stock[1];
					} else if(stock.length == "3") {
						code1 = stock[0];
						code2 = stock[1];
						code3 = stock[2];
					}
				}

				if(state == "1") {
					if(turnplate.bRotate) return;
					turnplate.bRotate = !turnplate.bRotate;
					//获取随机数(奖品个数范围内)
					var item = rnd(1, turnplate.restaraunts.length);
					//奖品数量等于10,指针落在对应奖品区域的中心角度[252, 216, 180, 144, 108, 72, 36, 360, 324, 288]

					//		rotateFn(2, turnplate.restaraunts[item - 1]);
					rotateFn(position, turnplate.restaraunts[item - 1]);

					$('#t_surplucounts').html(languages.surplucounts.replace("%1",result.surplucounts));
				} else if(state == "0") {
					alert(languages.alertText2);
				} else if(state == "2") {
					var jbs = $('#jbs').text();
					var a = window.confirm(languages.alertText3 + jbs + 
						languages.alertText4 + jbs + languages.alertText5);
					if(a == true) { // 进行购买
						isTurn=false;
						var t;	
						//截取字符串
//						ch = new Array; 
//						ch = cs.split("&"); 
//						var a1 = ch[0]; 
//						var a2 = ch[2];
						var canshu2 =cs;// a1+"&"+a2;
						var path2 = "c_buyxg_new.shop?"+canshu2;
						$.ajax({
							url: path2,
							dataType: "jsonp",
							jsonpCallback: "callback", //需要的回调函数
							success: function(data) {
								isTurn = true;
								t = data.state;
								if(t == "1") {
									alert(languages.alertText6);
								} else { 
									alert(languages.alertText7);
								}
								$('#t_surplucounts').html(languages.surplucounts.replace("%1",data.surplucounts));
							}
						});
					} else {
						isTurn = true;
						//alert(languages.alertText8);
					}
				} else if(state == "3") {
					alert(languages.alertText9);
					isTurn = true;
				}
			}
		});
	
	});
});


/**
 * 国际化 
 */
function globalI18n() {
	$('#t_surplucounts').html(languages.surplucounts.replace("%1",$('#surplucounts').text()));
	$('#guize').html(languages.guize);
	$('#jieshao').html(languages.jieshao);
	$('#guize_detail').html(languages.guize_detail);
	$('#turnType1').html(languages.turnType1);
	$('#turnType2').html(languages.turnType2);
	$('#turnType3').html(languages.turnType3);
	$('#turnType4').html(languages.turnType4);
	$('#turnType5').html(languages.turnType5);
	$('#turnType6').html(languages.turnType6);
	$('#turnType7').html(languages.turnType7);
	$('#ndxs_desc_title').html(languages.ndxs_desc_title);
	$('#ndxs_desc').html(languages.ndxs_desc);
	document.getElementById("zhizhen").src = languages.zhizhen;
	document.getElementById("bigImg").src = languages.bigImg;
}

/**
 * 判断是Android还是Ios平台
 */
function androidIos() {
	var device1 = $('#device').text();
	if (device1 == "1") {
		device = 1;
	} else if (device1 == "2") {
		device = 2;
	} else {
		device = 3;
	}
}

/**
 * 能否打开当前页面
 */
function canOpenPage() {
	var s;
	if (device == 2) {//Ios交互传来状态值
		s = jsobjectmodel.getZhuanGuState();
	} else if (device == 1) {//Android交互传来状态值
		s = window.wxc.getLoadHtmlState(); //转盘页面打开判断
	} else {
		s = "1";
	}

	if (s == "1") {
		drawRouletteWheel();

		//控制单选按钮
		var aCat = document.getElementsByName('r_sel');
		for ( var i = 0; i < aCat.length; i++) {
			aCat[i].onchange = function() {
				selectType = this.value;
			}
		}
	} else {
		$("body").html("");
		//		alert("很抱歉，您打开页面失败！");
	}
}

/**
 * 加载转股记录
 */
function loadZhuanGuRecord() {
	var path = "";
	if(device == 2) {//与IOS的交互
		//SelectedStockAction("SelectedStockAction");
		cs=jsobjectmodel.getZhuanGuParams();
		path = "c_xgrecordAll_new.shop?"+encodeURI(cs);
	} else if (device == 1) {//与Android的交互
		cs = window.wxc.getPlateRoateState();
		path = "c_xgrecordAll_new.shop?"+encodeURI(cs);
	} else {
		cs = "jwcode=7c4f52d2f8137c63443ec7998affd73faeee2d1c7b827ab4";
		path = "c_xgrecordAll_new.shop?"+encodeURI(cs);
	}
	
	$.ajax( {
		url : path,
		dataType : "jsonp",
		jsonpCallback : "callback", //需要的回调函数
		success : function(data) {
			var xin1 = $('#xinxi1').text(data[0]);
			var xin2 = $('#xinxi2').text(data[1]);
			var xin3 = $('#xinxi3').text(data[2]);
			var xin4 = $('#xinxi4').text(data[3]);
			var xin5 = $('#xinxi5').text(data[4]);
			var xin6 = $('#xinxi6').text(data[5]);
			var xin7 = $('#xinxi7').text(data[6]);
			var xin8 = $('#xinxi8').text(data[7]);
			var xin9 = $('#xinxi9').text(data[8]);
			var xin10 = $('#xinxi10').text(data[9]);
		}
	});
}

//生成的随机数可以控制大转盘可以转到哪个位置
function rnd(n, m) {
	var random = Math.floor(Math.random() * (m - n + 1) + n); //返回[1,9)范围的随机数
	return random;
}

window.onresize = function() {
	drawRouletteWheel();
}




function drawRouletteWheel() {
	//	dwidth = $("body").width() *0.9;
	// dwidth = 70; 
	//console.log(dwidth);

	var canvas = document.getElementById("wheelcanvas");
	//	canvas.width = dwidth;
	//	canvas.height = dwidth;
	dwidth = canvas.width;
	if(canvas.getContext) {
		//根据奖品个数计算圆周角度
		var arc = Math.PI / (turnplate.restaraunts.length / 2);
		var ctx = canvas.getContext("2d"); //获取绘图环境
		//在给定矩形内清空一个矩形
		ctx.clearRect(0, 0, dwidth, dwidth);
		//strokeStyle 属性设置或返回用于笔触的颜色、渐变或模式  
		ctx.strokeStyle = "#FFBE04";
		//font 属性设置或返回画布上文本内容的当前字体属性
		ctx.font = '18px Microsoft YaHei';
		for(var i = 0; i < turnplate.restaraunts.length; i++) {
			var angle = turnplate.startAngle + i * arc;
			ctx.fillStyle = turnplate.colors[i % 3];
			ctx.beginPath();
			//arc(x,y,r,起始角,结束角,绘制方向) 方法创建弧/曲线（用于创建圆或部分圆）    
			var outsideRadius = dwidth / 2 - dwidth * 0.025;
			var insideRadius = dwidth / 2 - dwidth * 0.356;
			ctx.arc(dwidth / 2, dwidth / 2, outsideRadius, angle, angle + arc, false);
			ctx.arc(dwidth / 2, dwidth / 2, insideRadius, angle + arc, angle, true);
			ctx.stroke();
			ctx.fill();
			//锁画布(为了保存之前的画布状态)
			ctx.save();
			//----绘制奖品开始----
			ctx.fillStyle = "#E5302F"; //设置整个画布的背景色
			var text = turnplate.restaraunts[i];
			var line_height = 16;
			//translate方法重新映射画布上的 (0,0) 位置
			var textRadius = dwidth / 2 * 0.7;
			ctx.translate(dwidth / 2 + Math.cos(angle + arc / 2) * textRadius, dwidth / 2 + Math.sin(angle + arc / 2) * textRadius);
			//rotate方法旋转当前的绘图
			ctx.rotate(angle + arc / 2 + Math.PI / 2);
			/** 下面代码根据奖品类型、奖品名称长度渲染不同效果，如字体、颜色、图片效果。(具体根据实际情况改变) **/
			 gethczpwords(ctx,text,line_height);
			//添加对应图标
//			if(text.indexOf("牛股") > 0) {
//				var img = document.getElementById("sorry-img");
//				img.onload = function() {
//					ctx.drawImage(img, -10, 15, 15, 15);
//				};
//				ctx.drawImage(img, -10, 15, 15, 15);
//			} else {
//				var img = document.getElementById("shan-img");
//				img.onload = function() {
//					ctx.drawImage(img, -10, 15, 15, 15);
//				};
//				ctx.drawImage(img, -10, 15, 15, 15);
//			}
			//把当前画布返回（调整）到上一个save()状态之前 
			ctx.restore();
			//----绘制奖品结束----
		}
	}
}
/**
 * 该方法用来对转盘中文字做回车处理的
 * @param ctx
 * @param text
 * @param line_height
 */
function gethczpwords(ctx,text,line_height){
	if(text.indexOf("牛股") > 0) { //流量包
		var texts = text.split("牛股");
		for(var j = 0; j < texts.length; j++) {
			ctx.font = j == 0 ? 'bold 14px Microsoft YaHei' : 'bold 14px Microsoft YaHei';//'14px Microsoft YaHei';
			if(j == 0) {
				ctx.fillText(texts[j], -ctx.measureText(texts[j]).width / 2, j * line_height);
			} else {
				ctx.fillText("牛股", -ctx.measureText("牛股").width / 2, j * line_height);
			}
		}
	} else if(text.indexOf("Bullish Stocks") > 0) { //流量包
		var texts = text.split("Bullish Stocks");
		for(var j = 0; j < texts.length; j++) {
			ctx.font = j == 0 ? 'bold 14px Microsoft YaHei' : 'bold 14px Microsoft YaHei';//'14px Microsoft YaHei';
			if(j == 0) {
				ctx.fillText(texts[j], -ctx.measureText(texts[j]).width / 2, j * line_height);
			} else {
				ctx.fillText("Bullish Stocks", -ctx.measureText("Bullish Stocks").width / 2, j * line_height);
			}
		}
	}else if(text.indexOf("ลุ้นรับเหรียญทอง") > 0) { //流量包
		var texts = text.split("ลุ้นรับเหรียญทอง");
		for(var j = 0; j < texts.length; j++) {
			ctx.font = j == 0 ? 'bold 14px Microsoft YaHei' : 'bold 14px Microsoft YaHei';//'14px Microsoft YaHei';
			if(j == 0) {
				ctx.fillText(texts[j], -ctx.measureText(texts[j]).width / 2, j * line_height);
			} else {
				ctx.fillText("ลุ้นรับเหรียญทอง", -ctx.measureText("ลุ้นรับเหรียญทอง").width / 2, j * line_height);
			}
		}
	}else if(text.indexOf("牛股") > 0) { //流量包
		var texts = text.split("牛股");
		for(var j = 0; j < texts.length; j++) {
			ctx.font = j == 0 ? 'bold 14px Microsoft YaHei' : 'bold 14px Microsoft YaHei';//'14px Microsoft YaHei';
			if(j == 0) {
				ctx.fillText(texts[j], -ctx.measureText(texts[j]).width / 2, j * line_height);
			} else {
				ctx.fillText("牛股", -ctx.measureText("牛股").width / 2, j * line_height);
			}
		}
	}else if(text.indexOf("Difference") > 0) { //流量包
		var texts = text.split("Difference");
		for(var j = 0; j < texts.length; j++) {
			ctx.font = j == 0 ? 'bold 14px Microsoft YaHei' : 'bold 14px Microsoft YaHei';//'14px Microsoft YaHei';
			if(j == 0) {
				ctx.fillText(texts[j], -ctx.measureText(texts[j]).width / 2, j * line_height);
			} else {
				ctx.fillText("Difference", -ctx.measureText("Difference").width / 2, j * line_height);
			}
		}
	}else if(text.indexOf("Attack") > 0) { //流量包
		var texts = text.split("Attack");
		for(var j = 0; j < texts.length; j++) {
			ctx.font = j == 0 ? 'bold 14px Microsoft YaHei' : 'bold 14px Microsoft YaHei';//'14px Microsoft YaHei';
			if(j == 0) {
				ctx.fillText(texts[j], -ctx.measureText(texts[j]).width / 2, j * line_height);
			} else {
				ctx.fillText("Attack", -ctx.measureText("Attack").width / 2, j * line_height);
			}
		}
	}else {
		ctx.font = 'bold 18px Microsoft YaHei';
		//在画布上绘制填色的文本。文本的默认颜色是黑色
		//measureText()方法返回包含一个对象，该对象包含以像素计的指定字体宽度
		ctx.fillText(text, -ctx.measureText(text).width / 2, 0);
	}
}