import approval

if __name__ == '__main__':
    app = approval.create_app()
    # from approval.models import Approval
    #
    # Approval.insert_approvals()
    app.run(debug=True)