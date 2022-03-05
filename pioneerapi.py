#!/usr/bin/env python

# cat <<EOF | tr -d ' ' | awk -F ':' '{ print "    \x27"$1"\x27" " \: " "\x27"$2"\x27," }'
# cat <<EOF | tr -d ' ' | awk -F ':' '{ print "\x27"$1"\x27," }' | tr '\n' ' '
INPUT_MODES= {
    '25' : 'BD',
    '04' : 'DVD',
    '06' : 'SAT/CBL',
    '15' : 'DVR/BDR',
    '10' : 'VIDEO1(VIDEO)',
    '19' : 'HDMI1',
    '20' : 'HDMI2',
    '21' : 'HDMI3',
    '22' : 'HDMI4',
    '23' : 'HDMI5',
    '24' : 'HDMI6',
    '34' : 'HDMI7',
    '35' : 'HDMI8',
    '26' : 'NETWORK(cyclic)',
    '38' : 'INTERNETRADIO',
    '41' : 'PANDORA',
    '44' : 'MEDIASERVER',
    '45' : 'FAVORITES',
    '17' : 'iPod/USB',
    '05' : 'TV',
    '01' : 'CD',
    '13' : 'USB-DAC',
    '02' : 'TUNER',
    '00' : 'PHONO',
    '12' : 'MULTICHIN',
    '33' : 'ADAPTERPORT',
    '48' : 'MHL',
    '31' : 'HDMI(cyclic)'
}

# cat <<EOF | awk -F ':\t' '{ print "    \x27"$1"\x27" " \: " "\x27"$2"\x27," }'
LISTENING_MODES = {
    '0001' : 'STEREO (cyclic)',
    '0010' : 'STANDARD (cyclic)',
    '0009' : 'STEREO (direct set)',
    '0011' : '(2ch source)',
    '0013' : 'PRO LOGIC2 MOVIE',
    '0018' : 'PRO LOGIC2x MOVIE',
    '0014' : 'PRO LOGIC2 MUSIC',
    '0019' : 'PRO LOGIC2x MUSIC',
    '0015' : 'PRO LOGIC2 GAME',
    '0020' : 'PRO LOGIC2x GAME',
    '0031' : 'PRO LOGIC2z HEIGHT',
    '0032' : 'WIDE SURROUND MOVIE',
    '0033' : 'WIDE SURROUND MUSIC',
    '0012' : 'PRO LOGIC',
    '0016' : 'Neo:6 CINEMA',
    '0017' : 'Neo:6 MUSIC',
    '0037' : 'Neo:X CINEMA',
    '0038' : 'Neo:X MUSIC',
    '0039' : 'Neo:X GAME',
    '0021' : '(Multi ch source)',
    '0022' : '(Multi ch source)+DOLBY EX',
    '0023' : '(Multi ch source)+PRO LOGIC2x MOVIE',
    '0024' : '(Multi ch source)+PRO LOGIC2x MUSIC',
    '0034' : '(Multi-ch Source)+PRO LOGIC2z HEIGHT',
    '0035' : '(Multi-ch Source)+WIDE SURROUND MOVIE',
    '0036' : '(Multi-ch Source)+WIDE SURROUND MUSIC',
    '0025' : '(Multi ch source)DTS-ES Neo:6',
    '0026' : '(Multi ch source)DTS-ES matrix',
    '0027' : '(Multi ch source)DTS-ES discrete',
    '0030' : '(Multi ch source)DTS-ES 8ch discrete',
    '0043' : '(Multi ch source)+Neo:X CINEMA ',
    '0044' : '(Multi ch source)+Neo:X MUSIC',
    '0045' : '(Multi ch source)+Neo:X GAME',
    '0100' : 'ADVANCED SURROUND (cyclic)',
    '0101' : 'ACTION',
    '0103' : 'DRAMA',
    '0118' : 'ADVANCED GAME',
    '0117' : 'SPORTS',
    '0107' : 'CLASSICAL',
    '0110' : 'ROCK/POP',
    '0112' : 'EXTENDED STEREO',
    '0003' : 'Front Stage Surround Advance',
    '0200' : 'ECO MODE (cyclic)',
    '0212' : 'ECO MODE 1',
    '0213' : 'ECO MODE 2',
    '0153' : 'RETRIEVER AIR',
    '0113' : 'PHONES SURROUND',
    '0050' : 'THX (cyclic)',
    '0051' : 'PROLOGIC + THX CINEMA',
    '0052' : 'PL2 MOVIE + THX CINEMA',
    '0053' : 'Neo:6 CINEMA + THX CINEMA',
    '0054' : 'PL2x MOVIE + THX CINEMA',
    '0092' : 'PL2z HEIGHT + THX CINEMA',
    '0055' : 'THX SELECT2 GAMES',
    '0068' : 'THX CINEMA (for 2ch)',
    '0069' : 'THX MUSIC (for 2ch)',
    '0070' : 'THX GAMES (for 2ch)',
    '0071' : 'PL2 MUSIC + THX MUSIC',
    '0072' : 'PL2x MUSIC + THX MUSIC',
    '0093' : 'PL2z HEIGHT + THX MUSIC',
    '0073' : 'Neo:6 MUSIC + THX MUSIC',
    '0074' : 'PL2 GAME + THX GAMES',
    '0075' : 'PL2x GAME + THX GAMES',
    '0094' : 'PL2z HEIGHT + THX GAMES',
    '0076' : 'THX ULTRA2 GAMES',
    '0077' : 'PROLOGIC + THX MUSIC',
    '0078' : 'PROLOGIC + THX GAMES',
    '0201' : 'Neo:X CINEMA + THX CINEMA',
    '0202' : 'Neo:X MUSIC + THX MUSIC',
    '0203' : 'Neo:X GAME + THX GAMES',
    '0056' : 'THX CINEMA (for multi ch)',
    '0057' : 'THX SURROUND EX (for multi ch)',
    '0058' : 'PL2x MOVIE + THX CINEMA (for multi ch)',
    '0095' : 'PL2z HEIGHT + THX CINEMA (for multi ch)',
    '0059' : 'ES Neo:6 + THX CINEMA (for multi ch)',
    '0060' : 'ES MATRIX + THX CINEMA (for multi ch)',
    '0061' : 'ES DISCRETE + THX CINEMA (for multi ch)',
    '0067' : 'ES 8ch DISCRETE + THX CINEMA (for multi ch)',
    '0080' : 'THX MUSIC (for multi ch)',
    '0081' : 'THX GAMES (for multi ch)',
    '0082' : 'PL2x MUSIC + THX MUSIC (for multi ch)',
    '0096' : 'PL2z HEIGHT + THX MUSIC (for multi ch)',
    '0083' : 'EX + THX GAMES (for multi ch)',
    '0097' : 'PL2z HEIGHT + THX GAMES (for multi ch)',
    '0084' : 'Neo:6 + THX MUSIC (for multi ch)',
    '0085' : 'Neo:6 + THX GAMES (for multi ch)',
    '0086' : 'ES MATRIX + THX MUSIC (for multi ch)',
    '0087' : 'ES MATRIX + THX GAMES (for multi ch)',
    '0088' : 'ES DISCRETE + THX MUSIC (for multi ch)',
    '0089' : 'ES DISCRETE + THX GAMES (for multi ch)',
    '0090' : 'ES 8CH DISCRETE + THX MUSIC (for multi ch)',
    '0091' : 'ES 8CH DISCRETE + THX GAMES (for multi ch)',
    '0204' : 'Neo:X CINEMA + THX CINEMA (for multi ch)',
    '0205' : 'Neo:X MUSIC + THX MUSIC (for multi ch)',
    '0206' : 'Neo:X GAME + THX GAMES (for multi ch)',
    '0005' : 'AUTO SURR/STREAM DIRECT (cyclic)',
    '0006' : 'AUTO SURROUND',
    '0151' : 'Auto Level Control (A.L.C.)',
    '0007' : 'DIRECT',
    '0008' : 'PURE DIRECT',
    '0152' : 'OPTIMUM SURROUND'
}

# cat <<EOF | awk -F ': ' '{ print "    \x27"$1"\x27" " \: " "\x27"$2"\x27," }'
PLAYING_MODES = {
    '0101' : '[)(]PLIIx MOVIE',
    '0102' : '[)(]PLII MOVIE',
    '0103' : '[)(]PLIIx MUSIC',
    '0104' : '[)(]PLII MUSIC',
    '0105' : '[)(]PLIIx GAME',
    '0106' : '[)(]PLII GAME',
    '0107' : '[)(]PROLOGIC',
    '0108' : 'Neo:6 CINEMA',
    '0109' : 'Neo:6 MUSIC',
    '010c' : '2ch Straight Decode',
    '010d' : '[)(]PLIIz HEIGHT',
    '010e' : 'WIDE SURR MOVIE',
    '010f' : 'WIDE SURR MUSIC',
    '0110' : 'STEREO',
    '0111' : 'Neo:X CINEMA',
    '0112' : 'Neo:X MUSIC',
    '0113' : 'Neo:X GAME',
    '1101' : '[)(]PLIIx MOVIE',
    '1102' : '[)(]PLIIx MUSIC',
    '1103' : '[)(]DIGITAL EX',
    '1104' : 'DTS Neo:6',
    '1105' : 'ES MATRIX',
    '1106' : 'ES DISCRETE',
    '1107' : 'DTS-ES 8ch ',
    '1108' : 'multi ch Straight Decode',
    '1109' : '[)(]PLIIz HEIGHT',
    '110a' : 'WIDE SURR MOVIE',
    '110b' : 'WIDE SURR MUSIC',
    '110c' : 'Neo:X CINEMA ',
    '110d' : 'Neo:X MUSIC',
    '110e' : 'Neo:X GAME',
    '0201' : 'ACTION',
    '0202' : 'DRAMA',
    '0208' : 'ADVANCEDGAME',
    '0209' : 'SPORTS',
    '020a' : 'CLASSICAL   ',
    '020b' : 'ROCK/POP   ',
    '020d' : 'EXT.STEREO  ',
    '020e' : 'PHONES SURR. ',
    '020f' : 'FRONT STAGE SURROUND ADVANCE',
    '0211' : 'SOUND RETRIEVER AIR',
    '0212' : 'ECO MODE 1',
    '0213' : 'ECO MODE 2',
    '0301' : '[)(]PLIIx MOVIE +THX',
    '0302' : '[)(]PLII MOVIE +THX',
    '0303' : '[)(]PL +THX CINEMA',
    '0305' : 'THX CINEMA',
    '0306' : '[)(]PLIIx MUSIC +THX',
    '0307' : '[)(]PLII MUSIC +THX',
    '0308' : '[)(]PL +THX MUSIC',
    '030a' : 'THX MUSIC',
    '030b' : '[)(]PLIIx GAME +THX',
    '030c' : '[)(]PLII GAME +THX',
    '030d' : '[)(]PL +THX GAMES',
    '0310' : 'THX GAMES',
    '0311' : '[)(]PLIIz +THX CINEMA',
    '0312' : '[)(]PLIIz +THX MUSIC',
    '0313' : '[)(]PLIIz +THX GAMES',
    '0314' : 'Neo:X CINEMA + THX CINEMA',
    '0315' : 'Neo:X MUSIC + THX MUSIC',
    '0316' : 'Neo:X GAMES + THX GAMES',
    '1301' : 'THX Surr EX',
    '1303' : 'ES MTRX +THX CINEMA',
    '1304' : 'ES DISC +THX CINEMA',
    '1305' : 'ES 8ch +THX CINEMA ',
    '1306' : '[)(]PLIIx MOVIE +THX',
    '1309' : 'THX CINEMA',
    '130b' : 'ES MTRX +THX MUSIC',
    '130c' : 'ES DISC +THX MUSIC',
    '130d' : 'ES 8ch +THX MUSIC',
    '130e' : '[)(]PLIIx MUSIC +THX',
    '1311' : 'THX MUSIC',
    '1313' : 'ES MTRX +THX GAMES',
    '1314' : 'ES DISC +THX GAMES',
    '1315' : 'ES 8ch +THX GAMES',
    '1319' : 'THX GAMES',
    '131a' : '[)(]PLIIz +THX CINEMA',
    '131b' : '[)(]PLIIz +THX MUSIC',
    '131c' : '[)(]PLIIz +THX GAMES',
    '131d' : 'Neo:X CINEMA + THX CINEMA',
    '131e' : 'Neo:X MUSIC + THX MUSIC',
    '131f' : 'Neo:X GAME + THX GAMES',
    '0401' : 'STEREO',
    '0402' : '[)(]PLII MOVIE',
    '0403' : '[)(]PLIIx MOVIE',
    '0405' : 'AUTO SURROUND Straight Decode',
    '0406' : '[)(]DIGITAL EX',
    '0407' : '[)(]PLIIx MOVIE',
    '0408' : 'DTS +Neo:6',
    '0409' : 'ES MATRIX',
    '040a' : 'ES DISCRETE',
    '040b' : 'DTS-ES 8ch ',
    '040e' : 'RETRIEVER AIR',
    '040f' : 'Neo:X CINEMA',
    '0501' : 'STEREO',
    '0502' : '[)(]PLII MOVIE',
    '0503' : '[)(]PLIIx MOVIE',
    '0504' : 'DTS/DTS-HD',
    '0505' : 'ALC Straight Decode',
    '0506' : '[)(]DIGITAL EX',
    '0507' : '[)(]PLIIx MOVIE',
    '0508' : 'DTS +Neo:6',
    '0509' : 'ES MATRIX',
    '050a' : 'ES DISCRETE',
    '050b' : 'DTS-ES 8ch ',
    '050e' : 'RETRIEVER AIR',
    '050f' : 'Neo:X CINEMA',
    '0601' : 'STEREO',
    '0602' : '[)(]PLII MOVIE',
    '0603' : '[)(]PLIIx MOVIE',
    '0605' : 'STREAM DIRECT NORMAL Straight Decode',
    '0606' : '[)(]DIGITAL EX',
    '0607' : '[)(]PLIIx MOVIE',
    '0609' : 'ES MATRIX',
    '060a' : 'ES DISCRETE',
    '060b' : 'DTS-ES 8ch ',
    '060c' : 'Neo:X CINEMA',
    '0701' : 'STREAM DIRECT PURE 2ch',
    '0702' : '[)(]PLII MOVIE',
    '0703' : '[)(]PLIIx MOVIE',
    '0704' : 'Neo:6 CINEMA',
    '0705' : 'STREAM DIRECT PURE Straight Decode',
    '0706' : '[)(]DIGITAL EX',
    '0707' : '[)(]PLIIx MOVIE',
    '0708' : '(nothing)',
    '0709' : 'ES MATRIX',
    '070a' : 'ES DISCRETE',
    '070b' : 'DTS-ES 8ch ',
    '070c' : 'Neo:X CINEMA',
    '0881' : 'OPTIMUM',
    '0e01' : 'HDMI THROUGH',
    '0f01' : 'MULTI CH IN'
}

class pioneerapi:

#Inquire
    qry_PowerStatus = '?P\r'
    qry_InputStatus = '?F\r'
    qry_VolumeStatus = '?V\r'
    qry_ListeningModeStatus = '?S\r'
    qry_PlayingModeStatus = '?L\r'
#Command
    cmd_PowerOn = 'PO\r'
    cmd_PowerOff = 'PF\r'
    cmd_PowerOnOff = 'PZ\r'

    def __init__(self):
        return

    def FL_decode(self, fl_text):
        decoded_fl = ''
        for i in range(2, 30, 2):
            char = fl_text[i:i+2]
            try:
                decoded_fl += chr(int(char,16))
            except KeyError:
                decoded_fl += '?'
        return decoded_fl

    def FN_decode(self,fn_text):
        decoded_fn = ''
        try:
            decoded_fn = INPUT_MODES[fn_text]
        except KeyError:
            decoded_fn = "INPUT KEY ERROR"
        return decoded_fn

    def SR_decode(self,sr_text):
        decoded_sr = ''
        try:
            decoded_sr = LISTENING_MODES[sr_text]
        except KeyError:
            decoded_sr = "LISTENING MODE KEY ERROR"
        return decoded_sr

    def LM_decode(self,lm_text):
        decoded_lm = ''
        try:
            decoded_lm = PLAYING_MODES[lm_text]
        except KeyError:
            decoded_lm = "PLAYING MODE KEY ERROR"
        return decoded_lm

    def RGB_decode(self,rgb_text):
        decoded_rgb = None
        if rgb_text[2:3] == '1':
            INPUT_MODES.update({rgb_text[0:2]:rgb_text[3:]})
            decoded_rgb = rgb_text
        return decoded_rgb

