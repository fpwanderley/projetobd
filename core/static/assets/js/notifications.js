/* ============================================================
 * Notifications
 * Triggers notifications using Pages Notification plugin.
 * ============================================================ */
(function($) {

    'use strict';

    $(document).ready(function() {

        $('.show-notification').click(function(e) {
            var title = $('.notification-title').val(); // Title to display inside the notification
            var message = $('.notification-message').val(); // Message to display inside the notification
            var type = $('.notification-type').val(); // Info, Success, Error etc
            var thumb =  $('.notification-thumb').val(); // Src to the thumbnail image

            $('body').pgNotification({
                style: 'circle',
                position: 'top-right',
                timeout: 5000,
                showClose: true,
                title: title,
                message: message,
                type: type,
                thumbnail: '<img width="40" height="40" style="display: inline-block;" src="' + thumb + '">'
            }).show();

            e.preventDefault();
        });

    });

})(window.jQuery);