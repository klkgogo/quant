import re

str = 'several reasons<font color="#CCCCCC"> the</font><font color="#E5E5E5"> first one in any</font>'

sub_str = re.sub(r'<[^>]+>', "", str)
print(sub_str)