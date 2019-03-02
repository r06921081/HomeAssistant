
from azure.storage.blob import BlockBlobService, PublicAccess


class sendPic():
  def __init__(self):
    self.block_blob_service = BlockBlobService(account_name='r06921058amewest', account_key='WZiLUEY+AnS9xZZ1iGMvjl5aDLIA41AVrpffy3kCuTv7KeNYtqwQgX3p8BYklMl/HbKDNwwTqayAjeaAtTFZLw==')
    self.container_name='photo'

  def uploadAndSendEmail(self, emails,filename,textBody):
    emailAddress=""
    for i in range(len(emails)):
        if i == 0:
            emailAddress=emailAddress+emails[i]+".jpg"
        else:
            emailAddress=emailAddress+','+emails[i]+'.jpg'
    emailAddress=emailAddress+"|"+textBody
    self.block_blob_service.create_blob_from_path(self.container_name, emailAddress,filename)
    #block_blob_service.create_blob_from_path(container_name, 'clothg34569@gmail.com.jpg,windwaker1121@hotmail.com.jpg', './clothg34569@gmail.png')
