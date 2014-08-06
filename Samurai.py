# -*- coding: utf-8 -*-
import sublime, sublime_plugin
import unicodedata
import re
from itertools import groupby

#######################################################################

class HighlightCharactersListener(sublime_plugin.EventListener):
    SETTINGS = sublime.load_settings('samurai.sublime-settings')
    # highlight full-pitch characters
    def highlight_fullpitch_characters(self, view):
        pattern = u'[　０-９Ａ-Ｚａ-ｚ]'
        view.add_regions('FullPitchWhiteSpaceHighlight',
                         view.find_all(pattern),
                         "comment",
                         sublime.DRAW_OUTLINED)

    # highlight unicode dependent characters
    def highlight_unicode_dependent_characters(self, view):
        pattern = u'[⅓-↟①-⓯☀-♯㈠-㉃㊀-㏾＇＂№℡ｱ-ﾝｯｧｨｩｪｫｬｭｮｰﾞﾟ]'
        view.add_regions('UnicodeDependentCharactersHighlight',
                         view.find_all(pattern),
                         "string",
                         sublime.DRAW_OUTLINED)

    # highlight platform dependent characters
    def highlight_platform_dependent_characters(self, view):
        pattern = u'[～∥－￠￡￢―➀➁➂➃➄➅➆➇➈➉俠俱剝吞啞噓嚙囊塡姸屛屢幷搔摑攢杮沪潑瀆焰瞱簞繡繫萊蔣蟬蠟軀醬醱頰顚驒鷗鹼麴䇳倂卽巢徵戾揭擊晚曆槪步歷每涉淚渴溫狀瘦硏禱緣虛錄鍊鬭麵黃欄廊虜殺類侮僧免勉勤卑喝嘆器塀墨層悔慨憎懲敏既暑梅海渚漢煮琢碑社祉祈祐祖祝禍禎穀突節練繁署者臭著褐視謁謹賓贈逸難響頻𠮟]'
        view.add_regions('PlatformDependentCharactersHighlight',
                         view.find_all(pattern),
                         "string",
                         sublime.DRAW_EMPTY_AS_OVERWRITE)

    # highlight uncompatible platform dependent characters
    def highlight_uncompatible_platform_dependent_characters(self, view):
        pattern = u'[纊褜鍈銈蓜俉炻昱棈鋹曻彅丨仡仼伀伃伹佖侒侊侚侔俍偀倢俿倞偆偰偂傔僴僘兊兤冝冾凬刕劜劦勀勛匀匇匤卲厓厲叝﨎咜咊咩哿喆坙坥垬埈埇﨏塚增墲夋奓奛奝奣妤妺孖寀甯寘寬尞岦岺峵崧嵓﨑嵂嵭嶸嶹巐弡弴彧德忞恝悅悊惞惕愠惲愑愷愰憘戓抦揵摠撝擎敎昀昕昻昉昮昞昤晥晗晙晴晳暙暠暲暿曺朎朗杦枻桒柀栁桄棏﨓楨﨔榘槢樰橫橆橳橾櫢櫤毖氿汜沆汯泚洄涇浯涖涬淏淸淲淼渹湜渧渼溿澈澵濵瀅瀇瀨炅炫焏焄煜煆煇凞燁燾犱犾猤猪獷玽珉珖珣珒琇珵琦琪琩琮瑢璉璟甁畯皂皜皞皛皦益睆劯砡硎硤硺礰礼神祥禔福禛竑竧靖竫箞精絈絜綷綠緖繒罇羡羽茁荢荿菇菶葈蒴蕓蕙蕫﨟薰蘒﨡蠇裵訒訷詹誧誾諟諸諶譓譿賰賴贒赶﨣軏﨤逸遧郞都鄕鄧釚釗釞釭釮釤釥鈆鈐鈊鈺鉀鈼鉎鉙鉑鈹鉧銧鉷鉸鋧鋗鋙鋐﨧鋕鋠鋓錥錡鋻﨨錞鋿錝錂鍰鍗鎤鏆鏞鏸鐱鑅鑈閒隆﨩隝隯霳霻靃靍靏靑靕顗顥飯飼餧館馞驎髙髜魵魲鮏鮱鮻鰀鵰鵫鶴鸙黑]'
        view.add_regions('UncompatiblePlatformDependentCharactersHighlight',
                         view.find_all(pattern),
                         "invalid",
                         sublime.DRAW_EMPTY_AS_OVERWRITE)

    # highlight characters
    def highlight_characters(self, view):
        if self.SETTINGS.get('highlight_full_pitch_characters', True):
            self.highlight_fullpitch_characters(view)
        if self.SETTINGS.get('highlight_unicode_dependent_characters', True):
            self.highlight_unicode_dependent_characters(view)
        if self.SETTINGS.get('highlight_platform_dependent_characters', True):
            self.highlight_platform_dependent_characters(view)
        if self.SETTINGS.get('highlight_uncompatible_platform_dependent_characters', True):
            self.highlight_uncompatible_platform_dependent_characters(view)

    # Called after changes have been made to a view.
    # @override
    def on_modified(self, view):
        self.highlight_characters(view)

    # Called when a view gains input focus.
    # @override
    def on_activated(self, view):
        self.highlight_characters(view)

    # Called when the file is finished loading.
    # @override
    def on_load(self, view):
        self.highlight_characters(view)

#######################################################################

class RegionRowPasteCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    list_replacements = sublime.get_clipboard().split("\n")
    num_of_reps = len(list_replacements)
    i = 0
    for my_selection in self.view.sel():
      if not my_selection.empty():
        if i < num_of_reps:
          self.view.replace(edit, my_selection, list_replacements[i])
        else:
          print("Placeholder["+str(i)+"] is not replaced.")
        i+=1

#------------------------------------------------------------------------

class RegionTsvPasteCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    list_replacements = re.split(u"[\n\t]",sublime.get_clipboard().strip())
    num_of_reps = len(list_replacements)
    i = 0
    for my_selection in self.view.sel():
      if not my_selection.empty():
        if i < num_of_reps:
          self.view.replace(edit, my_selection, list_replacements[i])
        else:
          print("Placeholder["+str(i)+"] is not replaced.")
        i+=1

#---------------------------------------------------------------------#

class TsvToTableCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    html = ""
    lines = sublime.get_clipboard().split("\n")
    for line in lines:
      columns = line.split("\t")
      parts = ""
      for column in columns:
        parts += "\t\t<td>%s</td>\n" % column.strip()
      html += "\t<tr>\n%s\t</tr>\n" % parts
    html = "<table>\n%s</table>" % html
    self.view.insert(edit, self.view.sel()[0].a, html)

#---------------------------------------------------------------------#

class AnchorPasteCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    anchor_url = sublime.get_clipboard()
    my_selection = self.view.sel()[0]
    my_text = self.view.substr(my_selection)
    if not my_selection.empty():
      self.view.replace(edit, my_selection, '<a href="'+anchor_url+'" target="_blank">'+my_text+'</a>')
    else:
      self.view.insert(edit, my_selection.a, '<a href="'+anchor_url+'" target="_blank">'+anchor_url+'</a>')

#######################################################################

class OverlapCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    my_selection = self.view.sel()[0]
    my_text = self.view.substr(my_selection)
    my_list = my_text.split('\n')
    my_list = [x for x,y in groupby(sorted(my_list)) if len(list(y)) > 1]
    self.view.replace(edit, my_selection, "\n".join(my_list))

class UniqCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    my_selection = self.view.sel()[0]
    my_text = self.view.substr(my_selection)
    my_list = my_text.split('\n')
    my_list = sorted(set(my_list), key=my_list.index)
    self.view.replace(edit, my_selection, "\n".join(my_list))

#######################################################################

class LinesToCommasCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    my_selection = self.view.sel()[0]
    my_text = self.view.substr(my_selection)
    my_list = my_text.split('\n')
    self.view.replace(edit, my_selection, ",".join(my_list))

#######################################################################

class CommasToLinesCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    my_selection = self.view.sel()[0]
    my_text = self.view.substr(my_selection)
    my_list = my_text.split(',')
    self.view.replace(edit, my_selection, "\n".join(my_list))

class LinesToCommaCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    my_selection = self.view.sel()[0]
    my_text = self.view.substr(my_selection)
    my_list = my_text.split('\n')
    self.view.replace(edit, my_selection, ",".join(my_list))

#######################################################################

class TabsToLinesCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    my_selection = self.view.sel()[0]
    my_text = self.view.substr(my_selection)
    my_list = my_text.split('\t')
    self.view.replace(edit, my_selection, "\n".join(my_list))

class LinesToTabsCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    my_selection = self.view.sel()[0]
    my_text = self.view.substr(my_selection)
    my_list = my_text.split('\n')
    self.view.replace(edit, my_selection, '\t'.join(my_list))

#######################################################################
# utility function
def replace(self, edit, find_str, replace_str):
  my_selection = self.view.sel()[0]
  view = self.view
  if my_selection.empty():
    view.sel().clear()
    matches = view.find_all(find_str)
    matches.reverse() #It must be replaced from the back.
    for region in matches:
      my_text = view.substr(region)
      my_text = my_text.replace(find_str,replace_str)
      view.replace(edit, region, my_text)
  else:
    my_text = view.substr(my_selection)
    my_text = my_text.replace(find_str,replace_str)
    view.replace(edit, my_selection, my_text)

#---------------------------------------------------------------------#

class NumericalCharacterReferenceCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    view = self.view
    my_selection = view.sel()[0]
    if not my_selection.empty():
      my_text = view.substr(my_selection)
      ncr = ''
      for c in my_text:
        ncr += hex(ord(c)).replace('0x', ('&#x'))+";"
      view.replace(edit, my_selection, ncr)

#---------------------------------------------------------------------#

class ConvertSafeStringCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    my_selection = self.view.sel()[0]
    view = self.view
    if my_selection.empty():
      view.sel().add(sublime.Region(0, view.size()))
      my_selection = view.sel()[0]
    my_text = view.substr(my_selection)
    my_dict = {
      u'➀' : '(1)', u'➁' : '(2)', u'➂' : '(3)', u'➃' : '(4)', u'➄' : '(5)',
      u'➅' : '(6)', u'➆' : '(7)', u'➇' : '(8)', u'➈' : '(9)', u'➉' : '(10)',
      u'～' : u'〜', u'－' : u'−', u'∥' : u'‖', u'￠' : u'¢', u'￡' : u'£',
      u'￢' : u'¬', u'―' : u'—', u'俠' : u'侠', u'俱' : u'倶', u'剝' : u'剥',
      u'吞' : u'呑', u'啞' : u'唖', u'噓' : u'嘘', u'嚙' : u'噛', u'囊' : u'嚢',
      u'塡' : u'填', u'姸' : u'妍', u'屛' : u'屏', u'屢' : u'屡', u'幷' : u'并',
      u'搔' : u'掻', u'摑' : u'掴', u'攢' : u'攅', u'杮' : u'柿', u'沪' : u'濾',
      u'潑' : u'溌', u'瀆' : u'涜', u'焰' : u'焔', u'瞱' : u'曄', u'簞' : u'箪',
      u'繡' : u'繍', u'繫' : u'繋', u'萊' : u'莱', u'蔣' : u'蒋', u'蟬' : u'蝉',
      u'蠟' : u'蝋', u'軀' : u'躯', u'醬' : u'醤', u'醱' : u'醗', u'頰' : u'頬',
      u'顚' : u'顛', u'驒' : u'騨', u'鷗' : u'鴎', u'鹼' : u'鹸', u'麴' : u'麹',
      u'䇳' : u'箋', u'倂' : u'併', u'卽' : u'即', u'巢' : u'巣', u'徵' : u'徴',
      u'戾' : u'戻', u'揭' : u'掲', u'擊' : u'撃', u'晚' : u'晩', u'曆' : u'暦',
      u'槪' : u'概', u'步' : u'歩', u'歷' : u'歴', u'每' : u'毎', u'涉' : u'渉',
      u'淚' : u'涙', u'渴' : u'渇', u'溫' : u'温', u'狀' : u'状', u'瘦' : u'痩',
      u'硏' : u'研', u'禱' : u'祷', u'緣' : u'縁', u'虛' : u'虚', u'錄' : u'録',
      u'鍊' : u'錬', u'鬭' : u'闘', u'麵' : u'麺', u'黃' : u'黄', u'欄' : u'欄',
      u'廊' : u'廊', u'虜' : u'虜', u'殺' : u'殺', u'類' : u'類', u'侮' : u'侮',
      u'僧' : u'僧', u'免' : u'免', u'勉' : u'勉', u'勤' : u'勤', u'卑' : u'卑',
      u'喝' : u'喝', u'嘆' : u'嘆', u'器' : u'器', u'塀' : u'塀', u'墨' : u'墨',
      u'層' : u'層', u'悔' : u'悔', u'慨' : u'慨', u'憎' : u'憎', u'懲' : u'懲',
      u'敏' : u'敏', u'既' : u'既', u'暑' : u'暑', u'梅' : u'梅', u'海' : u'海',
      u'渚' : u'渚', u'漢' : u'漢', u'煮' : u'煮', u'琢' : u'琢', u'碑' : u'碑',
      u'社' : u'社', u'祉' : u'祉', u'祈' : u'祈', u'祐' : u'祐', u'祖' : u'祖',
      u'祝' : u'祝', u'禍' : u'禍', u'禎' : u'禎', u'穀' : u'穀', u'突' : u'突',
      u'節' : u'節', u'練' : u'練', u'繁' : u'繁', u'署' : u'署', u'者' : u'者',
      u'臭' : u'臭', u'著' : u'著', u'褐' : u'褐', u'視' : u'視', u'謁' : u'謁',
      u'謹' : u'謹', u'賓' : u'賓', u'贈' : u'贈', u'逸' : u'逸', u'難' : u'難',
      u'響' : u'響', u'頻' : u'頻', u'𠮟' : u'叱'
    }
    rx = re.compile('|'.join(map(re.escape,my_dict)))  
    def one_xlat(match):
        return my_dict[match.group(0)]
    safechars = rx.sub(one_xlat, my_text)
    self.view.replace(edit, my_selection, safechars)

#---------------------------------------------------------------------#

class UnicodeNormalizeCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    my_selection = self.view.sel()[0]
    view = self.view
    if my_selection.empty():
      view.sel().add(sublime.Region(0, view.size()))
      my_selection = view.sel()[0]
    my_text = view.substr(my_selection)
    normalized = ''
    hankana_pattern = u'[ｱ-ﾝｯｧｨｩｪｫｬｭｮｰﾞﾟ]'
    hankana_re = re.compile(hankana_pattern)
    hankana = ''
    for c in my_text:
      if unicodedata.category(c) != 'Lu' and unicodedata.category(c) != 'Ll' and unicodedata.category(c) != 'Nd':
        if hankana_re.match(c):
          hankana += c
        else:
          if hankana:
            normalized += unicodedata.normalize('NFKC', hankana)
            hankana = ''
          normalized += unicodedata.normalize('NFKC', c)
      else:
          normalized += c
    self.view.replace(edit, my_selection, normalized)

#---------------------------------------------------------------------#

class UncompatibleGetalizeCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    my_selection = self.view.sel()[0]
    view = self.view
    if my_selection.empty():
      view.sel().add(sublime.Region(0, view.size()))
      my_selection = view.sel()[0]
    my_text = view.substr(my_selection)
    uncompatible_pattern = u'[纊褜鍈銈蓜俉炻昱棈鋹曻彅丨仡仼伀伃伹佖侒侊侚侔俍偀倢俿倞偆偰偂傔僴僘兊兤冝冾凬刕劜劦勀勛匀匇匤卲厓厲叝﨎咜咊咩哿喆坙坥垬埈埇﨏塚增墲夋奓奛奝奣妤妺孖寀甯寘寬尞岦岺峵崧嵓﨑嵂嵭嶸嶹巐弡弴彧德忞恝悅悊惞惕愠惲愑愷愰憘戓抦揵摠撝擎敎昀昕昻昉昮昞昤晥晗晙晴晳暙暠暲暿曺朎朗杦枻桒柀栁桄棏﨓楨﨔榘槢樰橫橆橳橾櫢櫤毖氿汜沆汯泚洄涇浯涖涬淏淸淲淼渹湜渧渼溿澈澵濵瀅瀇瀨炅炫焏焄煜煆煇凞燁燾犱犾猤猪獷玽珉珖珣珒琇珵琦琪琩琮瑢璉璟甁畯皂皜皞皛皦益睆劯砡硎硤硺礰礼神祥禔福禛竑竧靖竫箞精絈絜綷綠緖繒罇羡羽茁荢荿菇菶葈蒴蕓蕙蕫﨟薰蘒﨡蠇裵訒訷詹誧誾諟諸諶譓譿賰賴贒赶﨣軏﨤逸遧郞都鄕鄧釚釗釞釭釮釤釥鈆鈐鈊鈺鉀鈼鉎鉙鉑鈹鉧銧鉷鉸鋧鋗鋙鋐﨧鋕鋠鋓錥錡鋻﨨錞鋿錝錂鍰鍗鎤鏆鏞鏸鐱鑅鑈閒隆﨩隝隯霳霻靃靍靏靑靕顗顥飯飼餧館馞驎髙髜魵魲鮏鮱鮻鰀鵰鵫鶴鸙黑]'
    uncompatible_re = re.compile(uncompatible_pattern)
    getalized = ''
    for c in my_text:
      if uncompatible_re.match(c):
        getalized += u'〓'
      else:
        getalized += c
    self.view.replace(edit, my_selection, getalized)

#---------------------------------------------------------------------#

class AlnumNormalizeCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    my_selection = self.view.sel()[0]
    view = self.view
    if my_selection.empty():
      view.sel().add(sublime.Region(0, view.size()))
      my_selection = view.sel()[0]
    my_text = view.substr(my_selection)
    normalized = ''
    for c in my_text:
      if unicodedata.category(c) == 'Lu' or unicodedata.category(c) == 'Ll' or unicodedata.category(c) == 'Nd':
        normalized += unicodedata.normalize('NFKC', c)
      else:
        normalized += c
    self.view.replace(edit, my_selection, normalized)

#######################################################################
