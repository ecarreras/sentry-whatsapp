"""
sentry_whatsapp.models
~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2013 by Eduard Carreras, see AUTHORS for more details.
:license: BSD, see LICENSE for more details.
"""

import time

from django import forms
from django.core.urlresolvers import reverse

from sentry.plugins import Plugin
from sentry.utils.http import absolute_uri

import sentry_whatsapp
from sentry_whatsapp import WhatsappSender
        

class WhatsappOptionsForm(forms.Form):
    phone = forms.CharField(required=True, help_text="Your full phone number "
                            "including country code, without '+' or '00'")
    password = forms.CharField(help_text="Password to use for login.",
                           required=True)
    user = forms.CharField(help_text="User phone, with country code. Eg. "
                                     "34XXXXXXXXXYou can add multiple users "
                                     "to be notified separated by comma",
                           required=False)


class WhatsappMessage(Plugin):
    author = 'Eduard Carreras'
    author_url = 'https://github.com/ecarreras/sentry-whatsapp'
    title = 'Whatsapp'
    conf_title = 'Whatsapp'
    conf_key = 'whatsapp'
    version = sentry_whatsapp.VERSION
    project_conf_form = WhatsappOptionsForm


    def is_configured(self, project):
        go = self.get_option
        return (
            all(go(k, project) for k in ('phone', 'password'))
            and any(go(k, project) for k in ('user',))
        )

    def get_group_url(self, group):
        return absolute_uri(reverse('sentry-group', args=[
            group.team.slug,
            group.project.slug,
            group.id,
        ]))

    def post_process(self, group, event, is_new, is_sample, **kwargs):
        if not is_new or not self.is_configured(event.project):
            return
        link = self.get_group_url(group)
        message_format = '[%s] %s (%s)'
        message = message_format % (event.server_name, event.message, link)
        self.send_payload(event.project, message)

    def send_payload(self, project, message):
        login = self.get_option('phone', project)
        password = self.get_option('password', project)
        users = self.get_option('user', project)
        users = [x.strip() for x in users.split(',')]
        was = WhatsappSender(login, password)
        for phone in users:
            was.send(phone, message)
