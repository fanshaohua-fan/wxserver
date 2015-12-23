# -*- coding: utf-8 -*-
from base import db


class WeChatMessage(db.Model):
    __tablename__ = 'wechat_messages'

    id = db.Column(db.Integer, primary_key=True)
    ToUserName = db.Column(db.String(32), nullable=False)
    FromUserName = db.Column(db.String(32), nullable=False)
    CreateTime = db.Column(db.Integer, nullable=False)
    MsgType = db.Column(db.String(32), nullable=False)
    MsgId = db.Column(db.BigInteger, nullable=False)

    # text 
    Content = db.Column(db.String(2048))

    # image
    PicUrl = db.Column(db.String(255))
    MediaId = db.Column(db.String(255))

    # voice
    Format = db.Column(db.String(32))
    Recognition = db.Column(db.String(255))

    # video & shortvideo
    ThumbMediaId = db.Column(db.String(255))

    # location
    Location_X = db.Column(db.Float)
    Location_Y = db.Column(db.Float)
    Scale = db.Column(db.Integer)
    Label = db.Column(db.String(255))

    # link
    Title = db.Column(db.String(255))
    Description = db.Column(db.String(255))
    Url = db.Column(db.String(255))

    def __init__(self, **kw):
        self.ToUserName = kw['ToUserName']
        self.FromUserName = kw['FromUserName']
        self.CreateTime = kw['CreateTime']
        self.MsgType = kw['MsgType']
        self.MsgId = kw['MsgId']

        # text 
        if self.MsgType == 'text':
            self.Content = kw['Content']
        # image
        elif self.MsgType == 'image':
            self.PicUrl = kw['PicUrl']
            self.MediaId = kw['MediaId']
        # voice
        elif self.MsgType == 'voice':
            self.MediaId = kw['MediaId']
            self.Format = kw['Format']

            if kw.has_key('Recognition'):
                self.Recognition = kw['Recognition']
        # video & shortvideo
        elif self.MsgType == 'video' or self.MsgType == 'shortvideo':
            self.MediaId = kw['MediaId']
            self.ThumbMediaId = kw['ThumbMediaId']
        # location
        elif self.MsgType == 'location':
            self.Location_X = kw['Location_X']
            self.Location_Y = kw['Location_Y']
            self.Scale = kw['Scale']
            self.Label = kw['Label']
        # link
        elif self.MsgType == 'link':
            self.Title = kw['Title']
            self.Description = kw['Description']
            self.Url = kw['Url']
        else:
            pass


class WeChatEvent(db.Model):
    __tablename__ = 'wechat_events'

    id = db.Column(db.Integer, primary_key=True)
    ToUserName = db.Column(db.String(32), nullable=False)
    FromUserName = db.Column(db.String(32), nullable=False)
    CreateTime = db.Column(db.Integer, nullable=False)
    MsgType = db.Column(db.String(32), nullable=False)
    Event = db.Column(db.String(32), nullable=False)

    # SCAN
    EventKey = db.Column(db.String(255))
    Ticket = db.Column(db.String(255))
    # LOCATION
    Latitude = db.Column(db.Float)
    Longitude = db.Column(db.Float)
    Precision = db.Column(db.Float)
    # CLICK EventKey
    # VIEW EventKey

    def __init__(self, **kw):
        self.ToUserName = kw['ToUserName']
        self.FromUserName = kw['FromUserName']
        self.CreateTime = kw['CreateTime']
        self.MsgType = kw['MsgType']
        self.Event = kw['Event']

        if self.Event == 'CLICK' or self.Event == 'VIEW':
            self.EventKey = kw['EventKey']
        elif self.Event == 'SCAN':
            self.EventKey = kw['EventKey']
            self.Ticket = kw['Ticket']
        elif self.Event == 'LOCATION':
            self.Latitude = kw['Latitude']
            self.Longitude = kw['Longitude']
            self.Precision = kw['Precision']
        else:
            pass

