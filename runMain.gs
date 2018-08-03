/**
* @NotOnlyCurrentDoc
**/

messageList = [];

function putAuthor(document,name,color) {
  var nameStyle = {};
  nameStyle[DocumentApp.Attribute.FONT_FAMILY] = 'Arial';
  nameStyle[DocumentApp.Attribute.FONT_SIZE] = 14;
  nameStyle[DocumentApp.Attribute.BOLD] = true;
  nameStyle[DocumentApp.Attribute.FOREGROUND_COLOR] = color;
  
  document.appendParagraph(name).setAttributes(nameStyle);
}

function putContent(document, content) {
  if(content=='') {
    return false
  };
  var bodyStyle = {};
  bodyStyle[DocumentApp.Attribute.FOREGROUND_COLOR] = "#000000";
  bodyStyle[DocumentApp.Attribute.INDENT_START] = 15;
  bodyStyle[DocumentApp.Attribute.INDENT_FIRST_LINE] = 15;
  bodyStyle[DocumentApp.Attribute.FONT_SIZE] = 11;
  bodyStyle[DocumentApp.Attribute.BOLD] = false;
  
  document.appendParagraph(content).setAttributes(bodyStyle);
}

function putAttachments(document, attachments) {
  var attachmentStyle = {};
  attachmentStyle[DocumentApp.Attribute.FOREGROUND_COLOR] = "#1155cc";
  attachmentStyle[DocumentApp.Attribute.INDENT_FIRST_LINE] = 15;
  attachmentStyle[DocumentApp.Attribute.INDENT_START] = 15;
  attachmentStyle[DocumentApp.Attribute.FONT_SIZE] = 11;
  attachmentStyle[DocumentApp.Attribute.BOLD] = false;
  
  for(var i=0;i<attachments.length;i++) {
    attachmentStyle[DocumentApp.Attribute.LINK_URL] = attachments[i];
    document.appendParagraph("Attachment " + (i+1)).setAttributes(attachmentStyle);
  };
}

function putReactions(document, reactions) {
  if(reactions != "") {
    var reactionStyle = {};
    reactionStyle[DocumentApp.Attribute.FOREGROUND_COLOR] = "#000000"; 
    reactionStyle[DocumentApp.Attribute.INDENT_START] = 15;
    reactionStyle[DocumentApp.Attribute.INDENT_FIRST_LINE] = 15;
    reactionStyle[DocumentApp.Attribute.BOLD] = true;
  
    document.appendParagraph(reactions).setAttributes(reactionStyle);
  };
  
  document.appendParagraph("");
}


function putMessage(message,document) {
  putAuthor(document,message["authorName"],message["authorColor"]);
  putContent(document,message["messageContent"]);
  putAttachments(document,message["attachments"]);
  putReactions(document,message["reactions"]);
}

function uploadMessages(jsonInput) {
  var messageList = JSON.parse(jsonInput);
  var document = DocumentApp.create("Demo Document");
  const docID = document.getId();
  for(i=0;i<messageList.length;i++) {
    if(i%100 == 0) {
      document.saveAndClose();
      document = DocumentApp.openById(docID);
    };
    putMessage(messageList[i],document);
  };
  return true;
}