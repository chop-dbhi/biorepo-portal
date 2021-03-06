v1.0.5
---
* Updated support e-mail to eigsupport@email.chop.edu an added footer with new e-mail. #87
* Added institutional_email field to UserProfile model #86
* Fixed admin search function for ProtocolUserCredentialsAdmin, ProtocolDataSourceAdmin and ProtocolUserAdmin. #85 

v1.0.4
---
* Update ehb-datasources to 1.0.4 -- introduces improved driver exception handling

v1.0.3
---
* Representation of an Organization's Subject ID label is now rendered properly across all subject screens. #74
* Trim whitespace from Subject edit fields. #75
* Fixed an issue where updating a Subject would not update the corresponding Group for that
subject in the eHB which could cause subsequent issues creating new records for that subject. #76
* Add changelog view. #73

v1.0.2
---
* Add the ability to put the portal into "Maintenance Mode" by running the
`toggle_maintenance` Django management command. Ref #72
* ehb-datasources upgraded to v1.0.3 -- adds additional Nautilus mappings ehb-datasources/13
* Added notification of password expiry to LDAP backend. Ref #56
* Additional logging on dataentry views

v1.0.1
---
* Adds a django management command to reactivate locked out users. Ref Issue #67.
* Fixed issue where request body was not being properly decoded from bytes
to string preventing parsing json parsing and subsequently Subject Record
labels from being updated. Ref Issue #68
* Fixed Save and Continue not operating correctly due to CSRF token not being
available. Ref Issue #69
* Fixed issue with new Organization creation timing out. Ref Issue #70.

v1.0.0
---
* Initial Release
