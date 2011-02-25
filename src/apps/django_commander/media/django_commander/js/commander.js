var left = '#left', right = '#right';

function another_panel(selector) { return (selector==left) ? right : left; }
function remove_anchor(url) { return url.replace(/^.*#/, ''); }
function backup_hrefs(selector) {
	$(selector).find('a').each(function() { 
		var link = $(this);
		link.data('path',link.attr('href')); 
	});
}
function build_anchors(selector) {
	var panel = $(selector),
		another_path = $(another_panel(selector)).data('path');
		
	panel.find('.dir a').each(function(idx, val) {
		var link = $(this), anchor = '#';
		if (selector==left) { anchor = anchor + link.data('path') + '|' + another_path; }
		else { anchor = anchor + another_path + '|' + link.data('path'); }
		link.attr('href',anchor);
	});
}
		
function loadPanel(selector, path) {
	var pth;
	if (selector==left) { pth=path.split('|')[0]; }
	else { pth=path.split('|')[1]; }
	$.ajax({
		url: panel_url,
		data: {'path': pth},
		dataType: 'html',
		beforeSend: function() {
			$(selector).find('.panel-content').addClass('onload');
		},
		success: function(data) {
			var panel = $(selector);
			panel.html(data);
			panel.data('path',pth);
			backup_hrefs(selector);
			build_anchors(selector);
			build_anchors(another_panel(selector));
			panel.find('.dir a').click(function() {
				var url = remove_anchor($(this).attr('href'));
				$.history.load(url);
				return false;
			});
		},
		complete: function () {
			$(selector).find('.panel-content').removeClass('onload');
		}
	});			
}
		
$(function() {
	$(left).data('path','');
	$(right).data('path','');
    $.history.init(function(url) {
    	if (url=='') {
    		loadPanel(left, '|');
    		loadPanel(right, '|');
    	} else {
    		loadPanel(left, url);
    		loadPanel(right, url);
    	}
    });
});	