function _fixdd(){var ctx=parseInt($("span.xdiff").text());$("span.datex").each(function(){var dnn=$(this).text();var dnx=dnn;if(ctx>0)
{dnx=dnn+ctx;}
$(this).text(_format_date(dnx));});console.log(ctx);console.log("ff");$("span.datexbg").each(function(){var dnn=$(this).text();var dnx=dnn;if(1>0)
{}
$(this).text(_format_date(dnx));})}
function _format_date(unix_timestamp){var difference_in_seconds=(Math.round((new Date()).getTime()/1000))-unix_timestamp,current_date=new Date(unix_timestamp*1000),minutes,hours,months=new Array('January','February','March','April','May','June','July','August','September','October','November','December');if(difference_in_seconds<60){return "Just posted";}else if(difference_in_seconds<60*60){minutes=Math.floor(difference_in_seconds/60);return minutes+" min"+_plural(minutes)+" ago";}else if(difference_in_seconds<60*60*24){hours=Math.floor(difference_in_seconds/60/60);return hours+" hr"+_plural(hours)+" ago";}else if(difference_in_seconds>60*60*24){days=Math.floor(difference_in_seconds/60/60/24);return days+" day"+_plural(days)+" ago";return current_date.getDay()+" "+months[current_date.getMonth()].substr(0,3);}
return difference_in_seconds;function _fourdigits(number){return(number<1000)?number+1900:number;}
function _plural(number){if(parseInt(number)===1){return "";}
return "s";}}