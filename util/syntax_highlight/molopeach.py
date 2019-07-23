# -*- coding: utf-8 -*-
from pygments.style import Style
from pygments.token import Token, Comment, Name, Keyword, Generic, Number, Operator, String

class MolopeachStyle(Style):

    background_color = '#080808'
    styles = {
        Token:              '#fafafa bg:#080808',
        String:             '#eb007d',
        Comment:            '#6a6ad1',

        Name.Builtin:       '#64a3ce',
        Name.Constant:      '#eb007d',
        Name.Entity:        '#a772c8',
        Name.Tag:           '#ff9a00',
        #Name.Variable:      '#93e927',

        Keyword:            '#ff9a00',
        Keyword.Constant:   '#64a3ce',
        Keyword.Declaration:'#93e927',
        #Keyword.Type:       '#93e927',

        Comment.Preproc:    '#a772c8',
        Generic.Error:      '#dadae0 bg:#eb007d',
        Generic.Inserted:   'bg:#6a6ad1',
        Generic.Traceback:  '#dadae0 bg:#eb007d',
        Generic.Deleted:    '#6a6ad1 bg:#64a3ce',
        Generic.Subheading: '#a772c8',
        Generic.Heading:    '#a772c8',
        Generic.Output:     '#6a6ad1',
    }
