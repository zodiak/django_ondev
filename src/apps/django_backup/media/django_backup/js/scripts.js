$(function() {
	$('#action-toggle').click(function() {
		var targets = $('#list-rows input[type="checkbox"]');
		if ($(this).attr('checked')) {
			targets.attr('checked', true);
		} else {
			targets.removeAttr('checked');
		}
	});
	
	$('#delete-selected').click(function() {
		$('#selected_items').html($('#list-rows input[type="checkbox"]').clone());
	});
});
