<!doctype html>
<html>
<head>
  <title>{{title}}</title>
  <link rel="stylesheet" href="/css/whiteboard" />

% if defined('head'):
%    head()
% end

</head>
<body>
{{!base}}

% if defined('scripts'):
%   scripts()
% end
</body>
</html>
