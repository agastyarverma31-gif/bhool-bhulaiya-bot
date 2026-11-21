import discord
from discord.ext import commands
from discord.ui import Button, View, Modal, TextInput
import asyncio

# --- YAHAN APNI DETAILS BHARNI HAIN ---
TOKEN = "MTU3MzcyODMwMTgyMDgwOTIxNg.GLP2oj.3_pr34KvdrzyriVtLOM9BLAbLp0Glkg3BjKr4Y"  # Jo Step 1 mein copy kiya tha
STAFF_ROLE_ID = 1573731315964977162               # Neeche padho kaise nikalna hai
CATEGORY_ID = 1573731732140728340      # Neeche padho kaise nikalna hai
LOG_CHANNEL_ID = 1573731922721378405    # Neeche padho kaise nikalna hai

# --- BOT SETUP (ISE CHANGE MAT KARO) ---
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

# --- APPLICATION FORM (JAB KOI CLICK KAREGA) ---
class ApplicationModal(Modal, title="Bhool Bhulaiya SMP Application"):
    ign = TextInput(label="Minecraft Username (IGN)", placeholder="e.g. Notch", required=True, max_length=16)
    age = TextInput(label="How old are you?", placeholder="e.g. 16", required=True, max_length=2)
    reason = TextInput(label="Why do you want to join?", style=discord.TextStyle.paragraph, placeholder="Tell us a bit about yourself...", required=True, max_length=500)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message("✅ Application submitted! Wait for staff to review.", ephemeral=True)
        
        guild = interaction.guild
        category = discord.utils.get(guild.categories, id=CATEGORY_ID)
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            guild.get_role(STAFF_ROLE_ID): discord.PermissionOverwrite(read_messages=True, send_messages=True),
            interaction.user: discord.PermissionOverwrite(read_messages=True, send_messages=False)
        }
        
        ticket_channel = await guild.create_text_channel(
            name=f"app-{interaction.user.name}",
            category=category,
            overwrites=overwrites
        )
        
        embed = discord.Embed(title="📋 New SMP Application", color=discord.Color.purple())
        embed.add_field(name="Applicant", value=interaction.user.mention, inline=False)
        embed.add_field(name="IGN", value=self.ign.value, inline=True)
        embed.add_field(name="Age", value=self.age.value, inline=True)
        embed.add_field(name="Reason", value=self.reason.value, inline=False)
        
        view = StaffReviewView(applicant=interaction.user, ign=self.ign.value)
        await ticket_channel.send(embed=embed, view=view)

# --- STAFF KE BUTTONS (ACCEPT/REJECT) ---
class StaffReviewView(View):
    def __init__(self, applicant, ign):
        super().__init__(timeout=None)
        self.applicant = applicant
        self.ign = ign

    @discord.ui.button(label="Approve", style=discord.ButtonStyle.success, emoji="✅")
    async def approve(self, interaction: discord.Interaction, button: Button):
        try:
            await self.applicant.send(f"🎉 **Approved!** Welcome to Bhool Bhulaiya SMP!\n\nServer IP: `play.bhoolbhulaiya.fun`")
        except:
            pass
        log_channel = bot.get_channel(LOG_CHANNEL_ID)
        if log_channel:
            await log_channel.send(f"✅ {self.applicant.mention} approved by {interaction.user.mention}.")
        await interaction.response.send_message("Approved! Closing in 5s...")
        await asyncio.sleep(5)
        await interaction.channel.delete()

    @discord.ui.button(label="Deny", style=discord.ButtonStyle.danger, emoji="❌")
    async def deny(self, interaction: discord.Interaction, button: Button):
        try:
            await self.applicant.send("❌ Your application was Denied.")
        except:
            pass
        await interaction.response.send_message("Denied. Closing in 5s...")
        await asyncio.sleep(5)
        await interaction.channel.delete()

# --- THE MAIN APPLY BUTTON ---
class ApplyView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Apply for SMP", style=discord.ButtonStyle.primary, emoji="🎭", custom_id="apply_button_1")
    async def apply(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_modal(ApplicationModal())

# --- STARTUP ---
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    bot.add_view(ApplyView())

@bot.command()
@commands.has_permissions(administrator=True)
async def setup(ctx):
    embed = discord.Embed(
        title="🎭 Bhool Bhulaiya SMP Applications",
        description="Ready to enter the mystery? Click the button below to submit your application.\n\n**Requirements:**\n- Must have Discord\n- Be respectful\n- Ready to survive!",
        color=discord.Color.purple()
    )
    await ctx.send(embed=embed, view=ApplyView())
    await ctx.message.delete()

bot.run(TOKEN)
