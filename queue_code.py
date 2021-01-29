

def end_raid(self):
    members_in_raid = self.get_raid_party()
    for member in members_in_raid:
        # Raid ended so we are added 1 to their consecutive raids
        member.consecutive_raids = member.consecutive_raids + 1
        # If consecutive raids equals their rank's max consecutive raids they are sent back
        # to the end of the queue and their consecutive raid count is reset to zero
        if member.consecutive_raids == ROLE_RAIDS[member.cox_rank]:
            member.consecutive_raids = 0
            self.raid_queue.add_to_end_of_queue(member)
        else:
            # otherwise they are added back to the beginning of the queue
            self.raid_queue.add_to_start_of_queue(member)


def cancel_raid(self):
    members_in_raid = self.get_raid_party()
    for member in members_in_raid:
        self.raid_queue.add_to_start_of_queue(member)

@bot.command(name='endraid')
@commands.has_role('Pinkopia Admin')
async def end_raid(ctx):
    if "learner-raids-" in channel_name:
        global_raids_list[int(channel_name[-1]) - 1].end_raid()


        await ctx.channel.send("Raid has ended")


@bot.command(name='cancelraid')
@commands.has_role('Pinkopia Admin')
async def cancel_raid(ctx):
    if "learner-raids-" in channel_name:
        global_raids_list[int(channel_name[-1]) - 1].cancel_raid()


        await ctx.channel.send("Raid has been cancelled")
