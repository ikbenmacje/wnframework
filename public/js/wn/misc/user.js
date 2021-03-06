// misc user functions

wn.user_info = function(uid) {
	var def = {
		'fullname':uid, 
		'image': 'lib/images/ui/avatar.png'
	}
	if(!wn.boot.user_info) return def
	if(!wn.boot.user_info[uid]) return def
	if(!wn.boot.user_info[uid].fullname)
		wn.boot.user_info[uid].fullname = uid;
	if(!wn.boot.user_info[uid].image)
		wn.boot.user_info[uid].image = def.image;
	return wn.boot.user_info[uid];
}

wn.avatar = function(user, large, title) {
	var image = wn.utils.get_file_link(wn.user_info(user).image);
	var to_size = large ? 72 : 30;
	if(!title) title = wn.user_info(user).fullname;

	return repl('<span class="avatar" title="%(title)s" style="width: %(len)s; \
		height: %(len)s; border-radius: %(len)s; overflow: hidden;">\
		<img src="%(image)s"></span>', {
			image: image,
			len: to_size + "px",
			title: title
		});	
}

wn.provide('wn.user');

$.extend(wn.user, {
	name: (wn.boot ? wn.boot.profile.name : 'Guest'),
	has_role: function(rl) {
		if(typeof rl=='string') 
			rl = [rl];
		for(var i in rl) {
			if((wn.boot ? wn.boot.profile.roles : ['Guest']).indexOf(rl[i])!=-1)
				return true;
		}
	},
	get_desktop_items: function() {
		// get user sequence preference
		var user_list = wn.defaults.get_default("_desktop_items");
		if(user_list && user_list.length)
			var modules_list = user_list;

		if(modules_list) {
			// add missing modules - they will be hidden anyways by the view
			$.each(wn.modules, function(m, data) {
				if(modules_list.indexOf(m)==-1) {
					modules_list.push(m);
				}
			});
		}
		
		if(!modules_list || !modules_list.length) {
			// all modules
			modules_list = keys(wn.modules).sort();
		}
		
		// filter hidden modules
		if(wn.boot.hidden_modules && modules_list) {
			var hidden_list = JSON.parse(wn.boot.hidden_modules);
			var modules_list = $.map(modules_list, function(m) {
				if(hidden_list.indexOf(m)==-1) return m; else return null;
			});
		}

		// hide based on permission
		modules_list = $.map(modules_list, function(m) {
			var type = wn.modules[m] && wn.modules[m].type;
			var ret = null;
			switch(type) {
				case "module":
					if(wn.boot.profile.allow_modules.indexOf(m)!=-1)
						ret = m;
					break;
				case "page":
					if(wn.boot.allowed_pages.indexOf(wn.modules[m].link)!=-1)
						ret = m;
					break;
				case "view":
					ret = m;
					break;
				case "setup":
					ret = m;
					break;
				default:
					ret = null;
			}
			return ret;
		})

		return modules_list;
	},
	is_report_manager: function() {
		return wn.user.has_role(['Administrator', 'System Manager', 'Report Manager']);
	}
})

wn.session_alive = true;
$(document).bind('mousemove', function() {
	wn.session_alive = true;
	if(wn.session_alive_timeout) 
		clearTimeout(wn.session_alive_timeout);
	wn.session_alive_timeout = setTimeout('wn.session_alive=false;', 30000);
})