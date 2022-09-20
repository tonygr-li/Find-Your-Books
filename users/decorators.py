from django.shortcuts import redirect

def allowed_users(allowed_roles=[]):
	def decorator(view_func):
		def wrapper_func(request, *args, **kwargs):
			group = None

			if not request.user.groups.exists():
				return redirect('staff-only')

			if request.user.groups.exists():
				group = request.user.groups.all()

			j=False
			for i in group:
				if i.name in allowed_roles:
					j=True

			if j == True:
				return view_func(request, *args, **kwargs)
			else:
				return redirect('staff-only')
		return wrapper_func
	return decorator