package com.Project.InventoryManagement.Repository;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import com.Project.InventoryManagement.Entity.Product;



@Repository
public interface  ProductStockRepo extends JpaRepository<Product, Integer>{
    @Query(value="""
    SELECT p.productID, p.productName, p.productDesc, p.productType, s.quantity, p.price, s.rating 
    FROM Product p 
    JOIN Stock s ON p.productID = s.productID
    WHERE p.productID = :id
    """, nativeQuery = true)
    List<Object[]> findProductWithStockById(@Param("id") int id);

    @Query(value="""
    SELECT p.productID, p.productName, p.productDesc, p.productType, s.quantity, p.price, s.rating 
    FROM Product p 
    JOIN Stock s ON p.productID = s.productID
    WHERE p.productName = :name"""
    , nativeQuery = true)
    List<Object[]> findProductsWithStockByName(@Param("name") String name);

    @Query(value="""
    SELECT p.productID, p.productName, p.productDesc, p.productType, s.quantity, p.price, s.rating 
    FROM Product p 
    JOIN Stock s ON p.productID = s.productID
    WHERE p.productType = :type"""
    , nativeQuery = true)
    List<Object[]> findProductsWithStockByType(@Param("type") String type);

    @Query(value="""
    SELECT p.productID, p.productName, p.productDesc, p.productType, s.quantity, p.price, s.rating 
    FROM Product p 
    JOIN Stock s ON p.productID = s.productID
    WHERE p.productName = :name AND p.productType = :type
    """, nativeQuery=true)
    List<Object[]> findProductsWithStockByNameAndType(@Param("name") String name, @Param("type") String type);

    @Query(value="""
        SELECT p.productID, p.productName, p.productDesc, p.productType, s.quantity, p.price, s.rating 
        FROM Product p
        JOIN Stock s ON p.productID = s.productID
        """, nativeQuery = true)
    List<Object[]> findAllProductsWithStock();


}
