launch_auth: 
	cd ms_auth && uvicorn main:app --reload --port 8000


launch_skill: 
	cd ms_skill && uvicorn main:app --reload --port 8001