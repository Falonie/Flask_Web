var zlqiniu = {
    'setUp': function (args) {
        var domain = args['domain'];
        var params = {
            browse_button: args['browse_btn'],
            runtimes: 'html5,flash,html4',
            max_file_size: '500mb',
            dragdrop: false,
            chunk_size: '4mb',
            uptoken_url: args['uptoken_url'],
            domain: domain,
            get_new_uptoken: false,
            auto_start: true,
            unique_names: true,
            multi_selection: false,
            filters: {
                mime_types: [
                    {title: 'Image files', extensions: 'jpg,gif,png'},
                    {title: 'Video files', extensions: 'flv,mpg,mpeg,avi,wmv,mov,asf,rm,rmvb,mkv,mp4,m4v'}
                ]
            },
            log_level: 5,
            init: {
                'FileUploaded': function (up, file, info) {
                    if (args['success']) {
                        var success = args['success'];
                        file.name = domain + file.target_name;
                        success(up, file, info);
                    }
                },
                'Error': function (up, err, errTip) {
                    if (args['error']) {
                        var error = args['error'];
                        error(up, err, errTip);
                    }
                },
                'UploadProgress': function (up, file) {
                    if (args['progress']) {
                        args['progress'](up, file);
                    }
                },
                'FileAdded': function (up, files) {
                    if (args['fileadded']) {
                        args['fileadded'](up, files);
                    }
                },
                'UploadComplete': function () {
                    if (args['complete']) {
                        args['complete'](up, err, errTip);
                    }
                }
            }
        }
    }
};