import typing as t
from io import BytesIO, StringIO

from common.storage import storage
from servers.helpers.exceptions import BuilderNotFound

from .base import BaseBuilder, BuildStage


class MinecraftBuilder(BaseBuilder):
    def get_stages(self) -> t.List[BuildStage]:
        return [
            {
                'name': 'Create server.jar',
                'func': self._download_server,
            },
            {
                'name': 'Create running file',
                'func': self._create_dockerfile,
            },
            {
                'name': 'Accepting EULA',
                'func': self._create_eula,
            },
            {
                'name': 'Configurating',
                'func': self._init_server_properties,
            },
            {
                'name': 'Install plugins',
                'func': self._instal_plugins,
            },
        ]

    def _download_server(self) -> None:
        try:
            file_content = storage.read(self.server.version.filepath.path)
        except FileNotFoundError:
            raise BuilderNotFound('"server.jar" not found')
        self.files['server.jar'] = BytesIO(file_content)

    def _create_dockerfile(self) -> None:
        self.files['Dockerfile'] = StringIO('''FROM openjdk:8u212-jre-alpine
WORKDIR /home/app/
CMD ["java","-Xmx1024M","-Xms1024M","-jar","server.jar","nogui"]''')

    def _create_eula(self):
        self.files['eula.txt'] = StringIO('eula=TRUE')

    def _init_server_properties(self) -> None:
        self.files['server.properties'] = StringIO('''#Minecraft server properties
#Thu Jul 07 16:45:52 MSK 2016
spawn-protection=16
max-tick-time=-1
query.port=25565
generator-settings=
sync-chunk-writes=true
force-gamemode=false
allow-nether=true
enforce-whitelist=false
gamemode=survival
broadcast-console-to-ops=true
enable-query=false
player-idle-timeout=10
difficulty=easy
broadcast-rcon-to-ops=true
spawn-monsters=true
op-permission-level=4
pvp=true
snooper-enabled=false
level-type=default
hardcore=false
enable-command-block=false
network-compression-threshold=256
max-players=3
max-world-size=15000
resource-pack-sha1=
function-permission-level=2
rcon.port=25575
server-port=25565
server-ip=
spawn-npcs=true
allow-flight=false
level-name=world
view-distance=10
resource-pack=
spawn-animals=true
white-list=false
rcon.password=verySecretPassword
generate-structures=true
online-mode=false
max-build-height=256
level-seed=
prevent-proxy-connections=false
use-native-transport=true
motd=Donkey Engine server
enable-rcon=false''')

    def _instal_plugins(self):
        for mod in self.server.mods.all():
            try:
                file_content = storage.read(mod.mod.path)
            except FileNotFoundError:
                raise BuilderNotFound(f'"{mod.mod.path}" not found')
            self.files[f'plugins/{mod.name}.jar'] = BytesIO(file_content)
