<button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#exampleModal" data-bs-whatever="@mdo">Create Post</button>

        <div class="modal fade" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
          <div class="modal-dialog content">
            <div class="modal-content">
              <div class="modal-header">
                  <h5 class="modal-title" id="exampleModalLabel"><b>Create Post</b></h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
              </div>

              <div class="modal-body">
                <form method="post" enctype="multipart/form-data">
                    {% csrf_token %}
                  <div class="mb-3">
                    <input type="text" class="form-control" id="title" name="title" placeholder="Enter Post Title">
                  </div>
                  <div class="mb-3">
                    <textarea class="form-control" id="content" name="content" placeholder="Enter Post Content"></textarea>
                  </div>

                    <p class="mb-0">Select Category</p>
                    {% for category in categories %}
                        <div class="input-group-append mb-2">
                            <label class="mx-2" for="category">{{ category }}</label>
                            <input type="checkbox" class="category" name="category" onclick="checkCat(this)" value="{{ category }}"/>
                        </div>
                    {% endfor %}


                      <div class="input-group-append">
                        <input type="file" name="image" id="image" value="Choose image" />
                      </div>

                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                        <input type="submit" class="btn btn-primary" value="Post">
                    </div>
                </form>
              </div>


            </div>
          </div>
        </div>