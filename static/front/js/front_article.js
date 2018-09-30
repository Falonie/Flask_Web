// $(function () {
//     var ue = UE.getEditor('editor', {
//         'serverUrl': '/ueditor/upload/'
//     });
// });

$(function () {
    // $('#c').click(function (event) {
    $('#comment-btn').click(function (event) {
        event.preventDefault();
        var loginTag = $('#login-tag').attr("data-is-login");
        if (!loginTag) {
            window.location = '/signin/';
        } else {
            var contentInput = $("input[name='comment_content']");
            var content = contentInput.val();
            var post_id = $('#post-content').attr('data-id');
            zlajax.post({
                'url': '/comments/',
                'data': {
                    'comment_content': content,
                    'post_id': post_id
                },
                'success': function (data) {
                    if (data['code'] == 200) {
                        window.location.reload()
                    } else {
                        zlaleret.alertInfo(data['message']);
                    }
                }
            });
        }
    });
});