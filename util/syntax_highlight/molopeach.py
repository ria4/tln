# -*- coding: utf-8 -*-
from pygments.style import Style
from pygments.token import Token, Comment, Name, Keyword, Generic, Number, Operator, String

class MolopeachStyle(Style):

    background_color = '#101010'
    styles = {
        Token:              '#d0d0d0 bg:#101010',
        String:             '#960050',
        Comment:            '#3636b0',

        Name.Builtin:       '#3579a8',
        Name.Constant:      '#960050',
        Name.Entity:        '#7e40a5',
        Name.Tag:           '#c47f2c',
        #Name.Variable:      '#66aa11',

        Keyword:            '#c47f2c',
        Keyword.Constant:   '#3579a8',
        Keyword.Declaration:'#66aa11',
        #Keyword.Type:       '#66aa11',

        Comment.Preproc:    '#7e40a5',
        Generic.Error:      '#9999aa bg:#960050',
        Generic.Inserted:   'bg:#3636b0',
        Generic.Traceback:  '#9999aa bg:#960050',
        Generic.Deleted:    '#3636b0 bg:#3579a8',
        Generic.Subheading: '#7e40a5',
        Generic.Heading:    '#7e40a5',
        Generic.Output:     '#3636b0',
    }
