
# 3RD PARTY IMPORTS
from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

# LOCAL IMPORTS
from app import schemas, models, oauth2
from app.database import get_db

# BUILT-IN IMPORTS
...




# Create a Router for the app
router = APIRouter(prefix="/votes", tags=["Votes"])




# MAKE A VOTE
@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):


    # Build a query to find if the post intented to be voted existis
    post_query = db.query(models.Post).filter(models.Post.id == vote.post_id)
    
    # If the looked post doesn't exist
    if not post_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {vote.post_id}, does not exist")


    # Build the vote query to see if it exist already
    vote_query = db.query(models.Vote).filter(
        models.Vote.post_id == vote.post_id,
        models.Vote.user_id == current_user.id
    )

    # Store the DB retrival of the query
    found_vote = vote_query.first()


    # If the intention is to vote for the post
    if (vote.dir == 1):

        # If the user already voted for that post
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User '{current_user.id}' has already voted on post '{vote.post_id}'")

        # Otherwise, create the vote
        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)

        # Add the newly created vote to the DB and commit the change
        db.add(new_vote)
        db.commit()

        return {"message":"Successfully added vote!"}
    
    # If the intetion is to remove the vote from the post
    else:

        # if the vote doesn't exists        
        if not found_vote:            
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The vote trying to be deleted does not exist!")
        
        # Delete the vote found in DB & commit the change
        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message":"Successfully deleted vote!"}




