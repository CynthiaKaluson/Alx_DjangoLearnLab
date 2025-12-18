# Introduction to Django Project
## Permissions and Groups

Custom permissions were added to the Book model:
- can_view
- can_create
- can_edit
- can_delete

Groups created via Django Admin:
- Viewers: can_view
- Editors: can_view, can_create, can_edit
- Admins: can_view, can_create, can_edit, can_delete

Views are protected using Django's @permission_required decorator.
