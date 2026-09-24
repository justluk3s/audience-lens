# Useful Things

### Search

```
request = youtube.search().list(
        part="snippet",
        maxResults=25,
        q="jakidale"
    )
```


### Comment Thread

Choose what could be useful and what not

{
  "kind": "youtube#commentThread",
  "etag": "Iyv3SM_KRc2c7ag3ErLQA4qDRFY",
  "id": "Ugw-LCEldN-L9Cah8o54AaABAg",
  "snippet": {
    "channelId": "UCLtf1GhnARGHtP5jWcEmHLQ",
    "videoId": "kCoHipbcXFo",
    "topLevelComment": {
      "kind": "youtube#comment",
      "etag": "s8GzYF9h4Ke-S95XPbgCXmo-SOA",
      "id": "Ugw-LCEldN-L9Cah8o54AaABAg",
      "snippet": {
        "channelId": "UCLtf1GhnARGHtP5jWcEmHLQ",
        "videoId": "kCoHipbcXFo",
        "textDisplay": "Posso dire che, 1 gli inoob caricano una volta ogni morte di papa, ma quando caricano fanno dei capolavori. E 2 che i round cos\u00ec un po&#39; pi\u00f9 lunghi pi\u00f9 introspettivi che fanno vedere meglio i ragionamenti mi piacciono molto di pi\u00f9",
        "textOriginal": "Posso dire che, 1 gli inoob caricano una volta ogni morte di papa, ma quando caricano fanno dei capolavori. E 2 che i round cos\u00ec un po' pi\u00f9 lunghi pi\u00f9 introspettivi che fanno vedere meglio i ragionamenti mi piacciono molto di pi\u00f9",
        "authorDisplayName": "@francymega176",
        "authorProfileImageUrl": "https://yt3.ggpht.com/ytc/AIdro_kKUUdD-xv6qtNoZmM7xFr3UWTOcS0lCZqMKIFiW57O2OQ=s48-c-k-c0x00ffffff-no-rj",
        "authorChannelUrl": "http://www.youtube.com/@francymega176",
        "authorChannelId": {
          "value": "UC4tI1upPsuJFW7xOfc_xRLA"
        },
        "canRate": true,
        "viewerRating": "none",
        "likeCount": 0,
        "publishedAt": "2026-09-24T08:56:23Z",
        "updatedAt": "2026-09-24T08:56:23Z"
      }
    },
    "canReply": true,
    "totalReplyCount": 0,
    "isPublic": true
  }
}


# TO-DO List
- Understand how to storage the comments
- Undersand how to download quickly a big quantity of comments