$(document).ready(function(){
	
	
	
	$('#title').novacancy({
    'reblinkProbability': 0.1, //灯光闪烁的概率，取值0-1，默认值：1/3
    'blinkMin': 0.2,  //灯光闪烁的最小值。默认值0.01。单位：秒。
    'blinkMax': 0.6,  //灯光闪烁的最大值。默认值0.5。
    'loopMin': 0.5,  //触发霓虹灯闪烁的最小时间。默认值0.5。
    'loopMax': 1,
    'color': 'ORANGE', //灯光的颜色。默认值：'ORANGE'。
    'glow':  ['0 0 80px #ffffff', '0 0 30px #008000', '0 0 6px #0000ff'],   //文本阴影颜色数组。默认值： ['0 0 80px Orange', '0 0 30px Red', '0 0 6px Yellow']
    'off': 0,  //灯光熄灭的字符的数量。
    'blink': 0,  //灯光闪烁的字符的数量。默认值：0，0表示所有的字符都闪烁。
    'classOn': 'on',  //亮灯字符上的class名称。默认值： 'on'。
    'classOff': 'off',  //熄灯字符上的class名称。默认值：'off'。
    'autoOn': true     //是否在初始化后文字自动灯光闪烁。默认值：true。
});

$('#title').trigger('blinkOn'); 
	
});
