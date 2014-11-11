# -*- coding: utf-8 -*-

import base64
if __name__ == '__main__':
	print base64.b64encode("\n".join(open(u"Help.htm", 'r').readlines()))