import logging
import subprocess
import distutils.spawn
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction

logger = logging.getLogger(__name__)

class SystemManagementDirect(Extension):
  def __init__(self):
    logger.info('Carregando Extensão de configurações do Gnome')
    super(SystemManagementDirect, self).__init__()
    self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())

class KeywordQueryEventListener(EventListener):
  def on_event(self, event, extension):
    keyword = event.get_keyword()

    # Find the keyword id using the keyword (since the keyword can be changed by users)
    for id, kw in extension.preferences.items():
      if kw == keyword:
        self.on_match(id)
        return HideWindowAction()

  def on_match(self, id):
    if id == 'bloquear tela':
      subprocess.Popen(['loginctl', 'lock-session'])
    if id == 'suspender':
      subprocess.Popen(['systemctl', 'suspend', '-i'])
    if id == 'desligar':
      subprocess.Popen(['systemctl', 'poweroff', '-i'])
    if id == 'reiniciar':
      subprocess.Popen(['systemctl', 'reboot', '-i'])

SystemManagementDirect().run()
