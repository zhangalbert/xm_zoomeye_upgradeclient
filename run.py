 dict_conf = self.load_config()
        obj = type('obj', (object,), dict_conf)
        if not self.validate(obj) or dict_conf.get('email', None):
            fmtdata = (self.__class__.__name__,)
            msgdata = '{0} load invalid conf (smtp_host,smtp_port,smtp_user,smtp_pass,debug_num)'.format(*fmtdata)
            logger.error(msgdata)
            return

        mail_conf = dict_conf.get('email', None)
        if mail_conf is None:
            fmtdata = (self.__class__.__name__,)
            msgdata = '{0} load invalid conf (smtp_host,smtp_port,smtp_user,smtp_pass,debug_num)'.format(*fmtdata)
            logger.error(msgdata)
