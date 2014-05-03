from burrito.cmdsprovider import CmdsProvider

lastcmd = ['', '']

repeatables = (
    ":-) :) :o) :] :3 :c) :> =] 8) =) :} :^) :っ) "
    ":-D :D 8-D 8D x-D xD X-D XD =-D =D =-3 =3 B^D "
    ":-)) "
    ">:[ :-( :(  :-c :c :-<  :っC :< :-[ :[ :{ "
    ";( "
    ":-|| :@ >:( "
    ":'-( :'( "
    ":'-) :') "
    "D:< D: D8 D; D= DX v.v D-': "
    ">:O :-O :O :-o :o 8-0 O_O o-o O_o o_O o_o O-O "
    ":* :^* ( '}{' ) "
    ";-) ;) *-) *) ;-] ;] ;D ;^) :-, "
    ">:P :-P :P X-P x-p xp XP :-p :p =p :-Þ :Þ :þ :-þ :-b :b d: "
    ">:\ >:/ :-/ :-. :/ :\ =/ =\ :L =L :S >.< "
    ":| :-| "
    ":$ "
    ":-X :X :-# :# "
    "O:-) 0:-3 0:3 0:-) 0:) 0;^) "
    ">:) >;) >:-) "
    "}:-) }:) 3:-) 3:) "
    "o/\o ^5 >_>^ ^<_< "
    "|;-) |-O "
    ":-& :& "
    "#-) "
    "%-) %) "
    ":-###.. :###.. "
    "<:-| "
    "ಠ_ಠ "
    "<*)))-{ ><(((*> ><> "
    "\o/ "
    "*\0/* "
    "@}-;-'--- @>-->-- "
    "~(_8^(I) "
    "5:-) ~:-\ "
    "//0-0\\ "
    "*<|:-) "
    "=:o] "
    ",:-) 7:^] "
    "<3 </3 ").split()


class RepeatAfterTwo(CmdsProvider):
    respond_to_public = True
    cmds = {}

    def pre_process(self, command, conn_obj, data):
        # only need to keep track of the last two commands
        lastcmd[0], lastcmd[1] = lastcmd[1], command
        return command, data

    def match_command(self, command, conn_obj, data):
        last, this = lastcmd
        if last == this and this in repeatables:
            return self.cmd_repeat, command, data
        return None, None, data

    def cmd_repeat(self, command, data):
        reply = lastcmd[:1]
        # clear the latest data to avoid a premature repeated match
        lastcmd[1] = ''
        return reply
