import discord
import datetime
import psutil
import os

from ext.dataio import DataIO
from discord.ext import commands

class Utils (commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True)
    @commands.is_owner()
    async def maintenance(self, ctx):
        if self.bot.maintenance_mode is True:
            await self.bot.change_presence(
                status=discord.Status.online,
                game=None
            )

            self.bot.maintenance_mode = False

            await ctx.send('Maintenance mode off')

        else:
            await self.bot.change_presence(
                status=discord.Status.dnd,
                game=discord.Game(name='Maintenance...')
            )

            self.bot.maintenance_mode = True

            await ctx.send('Maintenance mode on')

    @commands.command()
    async def invite(self, ctx):
        perms = discord.Permissions.none()
        perms.read_messages = True
        perms.external_emojis = True
        perms.send_messages = True
        perms.attach_files = True
        perms.embed_links = True
        perms.manage_messages = True
        perms.add_reactions = True
        perms.administrator = True
        resp = f'{discord.utils.oauth_url(self.bot.user.id, perms)}'
        await ctx.send(resp)

    @commands.command(name='bot', aliases=['about', 'info', 'stats'])
    async def _bot(self, ctx):
        avatar_url = self.bot.user.avatar_url_as(static_format='jpg')
        prefix = (await self.bot.get_prefix(ctx.message))[2]
        em = discord.Embed()
        em.timestamp = datetime.datetime.utcnow()
        status = str(ctx.guild.me.status)
        if status == 'online':
            em.set_author(name="Bot Information", icon_url=avatar_url)
            em.color = discord.Color.green()
        elif status == 'dnd':
            status = 'maintenance'
            em.set_author(name="Bot Information", icon_url=None)
            em.color = discord.Color.purple()
        else:
            em.set_author(name="Bot Information", icon_url=avatar_url)
            em.color = discord.Color.red()

        total_online = len({m.id for m in self.bot.get_all_members() if m.status is not discord.Status.offline})
        total_unique = len(self.bot.users)
        channels = sum(1 for g in self.bot.guilds for _ in g.channels)

        now = datetime.datetime.utcnow()
        delta = now - self.bot.uptime
        hours, remainder = divmod(int(delta.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)

        fmt = '{h}h {m}m {s}s'
        if days:
            fmt = '{d}d ' + fmt
        uptime = fmt.format(d=days, h=hours, m=minutes, s=seconds)

        # TODO: Make a PSA command in dev.py this will currently be set by changing superclass PSA attribute via !eval
        psa = self.bot.psa
        if psa is None:
            psa = "Business as usual..."

        cmd = r'git show -s HEAD~3..HEAD --format="[{}](https://github.com/euab/the-oofster/commit/%H) %s (%cr)"'

        if os.name == 'posix':
            cmd = cmd.format(r'\`%h\`')
        else:
            cmd = cmd.format(r'`%h`')

        revision = os.popen(cmd).read().strip()

        em.add_field(name='PSA', value=psa, inline=False)
        em.add_field(name='Changelog', value=revision, inline=False)
        em.add_field(name='Current Status', value=str(status).title())
        em.add_field(name='Uptime', value=uptime)
        em.add_field(name='Latency', value=f'{self.bot.latency*1000:.2f} ms')
        em.add_field(name='Guilds', value=len(self.bot.guilds))
        em.add_field(name='Members', value=f'{total_online}/{total_unique} online')
        em.add_field(name='Channels', value=f'{channels} total')
        memory_usage = self.bot.process.memory_full_info().uss / 1024**2
        cpu_usage = self.bot.process.cpu_percent() / psutil.cpu_count()
        em.add_field(name='RAM Usage', value=f'{memory_usage:.2f} MiB')
        em.add_field(name='CPU Usage', value=f'{cpu_usage:.2f}% CPU Usage')
        em.add_field(name='Commands Run', value=sum(self.bot.commands_used.values()))
        em.add_field(name='GitHub', value='[Click Here](https://github.com/euab/the-oofster)')
        em.set_footer(text=f'{prefix}help')

        await ctx.send(embed=em)

    @commands.has_permissions(manage_guild=True)
    async def prefix(self, ctx, *, prefix):
        guild_id = str(ctx.guild.id)
        conf = DataIO.load_json("data/guild.json")
        conf[guild_id] = prefix
        DataIO.save_json(conf, "data/guild.json")
        await ctx.send(f'I changed your prefix to: `{prefix}`')

    @commands.command()
    async def ping(self, ctx):
        lat = f'{self.bot.latency * 1000:.4f} ms'
        await ctx.send('{} **Pong!** Message latency: {}'.format(
            ctx.author.mention,
            lat
        ))

def setup(bot):
    cog = Utils(bot)
    bot.add_cog(cog)
