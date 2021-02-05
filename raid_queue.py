
from collections import deque

MAX_PEOPLE = 7
ROLE_POINTS = {"Novice CoX": -4, "Beginner CoX": -4, "Intermediate CoX": -1, "Advanced CoX": 0, "Teacher CoX": 2}

# how many raids each rank get
ROLE_RAIDS = {"Novice CoX": 1, "Beginner CoX": 3, "Intermediate CoX": 3, "Advanced CoX": 4,
              "Teacher CoX": "unlimited"}

class RaidMember:
    def __init__(self, discord_name, rsn, cox_rank, consecutive_raids):
        self.discord_name = discord_name
        self.rsn = rsn
        self.cox_rank = cox_rank
        self.consecutive_raids = consecutive_raids

    def get_max_raids(self):
        return ROLE_RAIDS[self.cox_rank]

class RaidQueue(deque):


    def generate_party(self, teachers, current_members=None):
        if current_members:
            raid_party = current_members
            raid_party_points = raid_party.get_current_raid_party_points()
        else:
            raid_party = RaidParty()
            raid_party_points = 6

        for teacher in teachers:
            raid_party.append(teacher)
            raid_party_points += ROLE_POINTS[teacher.cox_rank]

        while len(raid_party) < MAX_PEOPLE and raid_party_points >= 0 and len(self) > 0:
            current_person = self.popleft()
            cox_rank = current_person.cox_rank

            raid_party_points += ROLE_POINTS[cox_rank]

            if len(raid_party) <= MAX_PEOPLE and raid_party_points >= 0:
                raid_party.append(current_person)
            else:
                self.appendleft(current_person)
        return raid_party



# a list with a few extra additions specific to representing a RaidParty
#raid party class will taken in the current queue and return a list of the current raid party

class RaidParty(list):

    def get_current_raid_party_points(self):
        current_points = 6
        for member in self:
            current_points += ROLE_POINTS[member.cox_rank]
        return current_points



# Overall class that represents a raids teaching session
# Contains a raid group and a raid queue
class RaidTeachingSession():

    def __init__(self, room_name):
        self.room_name = room_name
        self.raid_queue = RaidQueue()
        self.raid_party = RaidParty()
        self.accepting = False
        self.teachers = []

    def add_teacher(self, discord_name, rsn):
        new_member = RaidMember(discord_name, rsn, "Teacher CoX", 0)
        self.teachers.append(new_member)

    def open_queue(self):
        self.accepting = True

    def close_queue(self):
        self.accepting = False

    def get_status(self):
        return self.accepting

    def get_teachers(self):
        return self.teachers


    def add_to_queue(self, discord_name, rsn, cox_rank, consecutive_raids=0):
        new_member = RaidMember(discord_name, rsn, cox_rank, consecutive_raids)
        self.raid_queue.append(new_member)

    #returns the queue
    def get_raid_queue(self):
        queue = self.raid_queue
        return queue

    #returns the current raid party
    def get_raid_party(self):
        party = self.raid_party
        return party

    def generate_next_party(self):
        #getting raid_party_list defined in the RaidQueue class
        # get_raid_party() also pops off the list from the RaidQueue
        party_members = self.raid_queue.generate_party(self.teachers, self.raid_party)
        self.raid_party = party_members

    def end_raid(self):
        remove_list = []
        for member in self.raid_party:
            if member.cox_rank != "Teacher CoX":
                print(str(member.consecutive_raids))
                member.consecutive_raids = member.consecutive_raids + 1
                if member.consecutive_raids == ROLE_RAIDS[member.cox_rank]:
                    print(str(member.cox_rank))
                    member.consecutive_raids = 0
                    remove_list.append(member)
        for raid_member in remove_list:
            self.raid_party.remove(raid_member)
            self.raid_queue.append(raid_member)
        for member in self.raid_party:
            if member.cox_rank == "Teacher CoX":
                self.raid_party.remove(member)

    def cancel_raid(self):
        members_in_raid = self.get_raid_party()
        extending_list = []
        for member in members_in_raid:
            extending_list.append(member)
        extending_list.reverse()
        self.raid_queue.extendleft(extending_list)

    def remove_user(self, rsn):
        for member in self.raid_party:
            if rsn == member.rsn:
                self.raid_party.remove(member)

                return [True, "party"]
        for member in self.raid_queue:
            if rsn == member.rsn:
                self.raid_queue.remove(member)
                return [True, "queue"]
        return [False]


        #returns true if user found
        #retuns false if user not found

    def leave_queue(self, rsn):
        for member in self.raid_queue:
            if rsn == member.rsn:
                print("test")
                self.raid_queue.remove(member)
                return True
        return False

    def leave_teacher(self, rsn):
        for teacher in self.teachers:
            if rsn == teacher.rsn:
                self.teachers.remove(teacher)
                return True
        return False