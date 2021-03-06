from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from pkg_resources import require

import products
from .models import Product, Category, Review
from .forms import ProductForm, ReviewForm


def all_products(request):
    """ A view to show all products, including sorting and search queries """
    products = Product.objects.all()
    query = None
    categories = None
    sort = None
    direction = None

    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_product_name'
                products = products.annotate(lower_name=Lower('product_name'))

            if sortkey == 'category':
                sortkey = "product_category"

            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'

            products = products.order_by(sortkey)

        if 'category' in request.GET:
            category = request.GET['category'].split(',')
            products = products.filter(
                product_category__product_category__in=category)
            categories = Category.objects.filter(
                product_category__in=category)

            if 'direction' in request.GET:
                direction = request.GET['direction']
                sortkey = "product_category"
                if direction == "desc":
                    sortkey = f'-{sortkey}'

                products = products.order_by(sortkey)

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(
                    request, "You didn't enter any search criteria!")
                return redirect(reverse('products'))

            queries = Q(product_name__icontains=query) | Q(
                product_description__icontains=query)
            products = products.filter(queries)

    current_sorting = f'{sort}_{direction}'

    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories,
        'current_sorting': current_sorting,
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """ A view to show individual product details """

    # Query product from db
    product = get_object_or_404(Product, pk=product_id)
    # Query product's reviews from db
    reviews = Review.objects.all()
    reviews = reviews.filter(product=product)
    # Create Review form for posting reviews
    form = ReviewForm()

    # Context
    context = {
        "form": form,
        'product': product,
        "reviews": reviews,
    }

    return render(request, 'products/product_detail.html', context)


@login_required
@staff_member_required
def add_product(request):
    """ Add a product to the store """

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Successfully added product!')
            return redirect(reverse('product_detail', args=(product.id,)))
        else:
            messages.error(
                request, 'Failed to add product. Please ensure the form is valid.')
    else:
        form = ProductForm()

    template = 'products/add_product.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
@staff_member_required
def edit_product(request, product_id):
    """ Edit a product in the store """

    # Query product from db to be edited
    product = get_object_or_404(Product, pk=product_id)

    if request.method == 'POST':
        # Create Product form and pass it data received
        form = ProductForm(request.POST, request.FILES, instance=product)

        # Check if the form data is valid
        if form.is_valid():
            # If valid save
            form.save()

            messages.success(request, 'Successfully updated product!')

            return redirect(reverse('product_detail', args=(product.id,)))
        else:
            messages.error(
                request, 'Failed to update product. Please ensure the form is valid.')
    else:
        form = ProductForm(instance=product)

    template = 'products/edit_product.html'
    context = {
        'form': form,
        'product': product,
    }

    return render(request, template, context)


@login_required
@staff_member_required
def delete_product(request, product_id):
    """ Delete a product from the store """

    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    messages.success(request, 'Product deleted!')
    return redirect(reverse('products'))


@login_required
@require_POST
def add_review(request, product_id):
    """add review to product"""

    reviewForm = ReviewForm(request.POST or None)
    # Check if the review form inputs are valid
    if reviewForm.is_valid():
        # Get body context of the review
        body = request.POST.get("body")

        # Query product that is being reviewed
        product = get_object_or_404(Product, pk=product_id)

        # Create a review object
        review = Review.objects.create(
            product=product, user=request.user, body=body)
        review.save()
        return redirect(reverse("product_detail", args=(product_id,)))
    else:
        return redirect(reverse("product_detail", args=(product_id,)))


@login_required
def edit_review(request, review_id):
    """Edit Review of a product"""
    # Review to be edited
    review = get_object_or_404(Review, pk=review_id)

    # All Reviews
    reviews = Review.objects.all()

    # Product that is reviewed
    product = get_object_or_404(Product, pk=review.product.id)

    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)

        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated review!')
            return redirect(reverse('product_detail', args=(product.id,)))
        else:
            messages.error(
                request, 'Failed to update Review. Please ensure the form is valid.')

    form = ReviewForm(instance=review)
    template = 'products/product_detail.html'
    # Context
    context = {
        "form": form,
        'product': product,
        "reviews": reviews,
        "edit": "true",
        "edit_id": review.id,
    }

    return render(request, template, context)


@login_required
def delete_review(request, review_id):
    """Delete review"""

    # Find Review
    review = get_object_or_404(Review, pk=review_id)

    # Extract product id for redirecting
    product_id = review.product.id

    # Check if the user has the auth right to remove the review
    if review.user.id == request.user.id:
        review.delete()
        messages.success(request, "Review Deleted!")
        return redirect(reverse("product_detail", args=(product_id,)))
    else:
        messages.warning(request, "You don't have authorization to do that.")
        return redirect(reverse("product_detail", args=(product_id,)))